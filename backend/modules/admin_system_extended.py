# ===== DISCOUNT ROI TRACKING =====

@router.get("/admin/discounts/roi-tracking")
async def get_discount_roi_tracking(
    date_from: Optional[str] = Query(None),
    date_to: Optional[str] = Query(None),
    current_user: UserProfile = Depends(require_role([UserRole.ADMIN, UserRole.SUPER_ADMIN]))
):
    """Get ROI tracking for all discounts"""
    
    # Set default date range (last 90 days)
    if not date_from:
        date_from = (datetime.utcnow() - timedelta(days=90)).isoformat()
    if not date_to:
        date_to = datetime.utcnow().isoformat()
    
    date_filter = {
        "applied_at": {
            "$gte": datetime.fromisoformat(date_from.replace('Z', '+00:00')),
            "$lte": datetime.fromisoformat(date_to.replace('Z', '+00:00'))
        }
    }
    
    # Get all discount usage in period
    usage_data = await db.discount_usage.find(date_filter).to_list(length=50000)
    
    # Group by discount
    discount_roi = {}
    for usage in usage_data:
        discount_id = usage["discount_id"]
        if discount_id not in discount_roi:
            discount_roi[discount_id] = {
                "discount_id": discount_id,
                "total_uses": 0,
                "revenue_impact": 0.0,
                "users_acquired": set(),
                "conversion_rate": 0.0
            }
        
        discount_roi[discount_id]["total_uses"] += 1
        discount_roi[discount_id]["users_acquired"].add(usage["user_id"])
        
        # Calculate revenue impact
        if usage["discount_type"] == "percentage":
            estimated_value = 149.0 * (usage["discount_amount"] / 100)
        elif usage["discount_type"] == "fixed_amount":
            estimated_value = usage["discount_amount"]
        else:  # free_months
            estimated_value = 149.0 * usage["discount_amount"]
        
        discount_roi[discount_id]["revenue_impact"] += estimated_value
    
    # Get discount details and calculate final metrics
    roi_results = []
    for discount_id, data in discount_roi.items():
        discount = await db.discounts.find_one({"discount_id": discount_id})
        if discount:
            unique_users = len(data["users_acquired"])
            
            # Calculate estimated acquisition cost (simplified)
            estimated_cost = data["revenue_impact"] * 0.3  # Assume 30% cost ratio
            roi_percentage = ((data["revenue_impact"] - estimated_cost) / estimated_cost * 100) if estimated_cost > 0 else 0
            
            roi_results.append({
                "discount_name": discount["name"],
                "discount_id": discount_id,
                "total_uses": data["total_uses"],
                "unique_users": unique_users,
                "revenue_impact": round(data["revenue_impact"], 2),
                "estimated_cost": round(estimated_cost, 2),
                "roi_percentage": round(roi_percentage, 2),
                "cost_per_acquisition": round(estimated_cost / unique_users, 2) if unique_users > 0 else 0
            })
    
    # Sort by ROI percentage
    roi_results.sort(key=lambda x: x["roi_percentage"], reverse=True)
    
    return {
        "roi_tracking": roi_results,
        "period": f"{date_from} to {date_to}",
        "total_discounts_analyzed": len(roi_results)
    }

# ===== EXPORT CAPABILITIES =====

@router.post("/admin/export")
async def export_admin_data(
    export_request: ExportRequest,
    current_user: UserProfile = Depends(require_role([UserRole.ADMIN, UserRole.SUPER_ADMIN]))
):
    """Export admin data in various formats"""
    
    export_type = export_request.export_type
    filters = export_request.filters
    format_type = export_request.format
    
    # Build query based on filters
    query = {}
    if filters.get("date_range"):
        date_range = filters["date_range"]
        if date_range.get("from"):
            query.setdefault("created_at", {})["$gte"] = datetime.fromisoformat(date_range["from"])
        if date_range.get("to"):
            query.setdefault("created_at", {})["$lte"] = datetime.fromisoformat(date_range["to"])
    
    # Export users data
    if export_type == "users":
        if filters.get("subscription_tier"):
            query["subscription_tier"] = filters["subscription_tier"]
        if filters.get("is_active") is not None:
            query["is_active"] = filters["is_active"]
        
        users = await db.users.find(query).to_list(length=100000)
        
        # Remove sensitive data
        for user in users:
            user.pop("password_hash", None)
            user.pop("_id", None)
        
        if format_type == "csv":
            return _export_to_csv(users, "users_export")
        else:
            return {"data": users, "count": len(users)}
    
    # Export discounts data
    elif export_type == "discounts":
        discounts = await db.discounts.find(query).to_list(length=10000)
        
        # Get usage statistics for each discount
        for discount in discounts:
            discount.pop("_id", None)
            usage_count = await db.discount_usage.count_documents({"discount_id": discount["discount_id"]})
            discount["actual_usage_count"] = usage_count
        
        if format_type == "csv":
            return _export_to_csv(discounts, "discounts_export")
        else:
            return {"data": discounts, "count": len(discounts)}
    
    # Export banners data
    elif export_type == "banners":
        banners = await db.banners.find(query).to_list(length=10000)
        for banner in banners:
            banner.pop("_id", None)
        
        if format_type == "csv":
            return _export_to_csv(banners, "banners_export")
        else:
            return {"data": banners, "count": len(banners)}
    
    # Export analytics data
    elif export_type == "analytics":
        # Get comprehensive analytics
        total_users = await db.users.count_documents({})
        total_discounts = await db.discounts.count_documents({})
        total_banners = await db.banners.count_documents({})
        
        analytics_data = [{
            "metric": "Total Users",
            "value": total_users,
            "export_timestamp": datetime.utcnow().isoformat()
        }, {
            "metric": "Total Discounts",
            "value": total_discounts,
            "export_timestamp": datetime.utcnow().isoformat()
        }, {
            "metric": "Total Banners", 
            "value": total_banners,
            "export_timestamp": datetime.utcnow().isoformat()
        }]
        
        if format_type == "csv":
            return _export_to_csv(analytics_data, "analytics_export")
        else:
            return {"data": analytics_data, "count": len(analytics_data)}
    
    else:
        raise HTTPException(status_code=400, detail="Invalid export type")

def _export_to_csv(data, filename):
    """Helper function to export data as CSV"""
    if not data:
        raise HTTPException(status_code=400, detail="No data to export")
    
    # Create CSV content
    output = io.StringIO()
    
    # Get field names from first record
    fieldnames = list(data[0].keys())
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    
    writer.writeheader()
    for row in data:
        # Convert datetime objects to strings
        cleaned_row = {}
        for key, value in row.items():
            if isinstance(value, datetime):
                cleaned_row[key] = value.isoformat()
            elif isinstance(value, list):
                cleaned_row[key] = ", ".join(str(item) for item in value)
            else:
                cleaned_row[key] = value
        writer.writerow(cleaned_row)
    
    # Create response
    csv_content = output.getvalue()
    output.close()
    
    return StreamingResponse(
        io.StringIO(csv_content),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.csv"}
    )

# ===== ADVANCED BANNER SCHEDULING =====

@router.post("/admin/banners/{banner_id}/schedule")
async def schedule_banner(
    banner_id: str,
    schedule_config: Dict[str, Any],
    current_user: UserProfile = Depends(require_role([UserRole.ADMIN, UserRole.SUPER_ADMIN]))
):
    """Advanced banner scheduling with recurrence options"""
    
    banner = await db.banners.find_one({"banner_id": banner_id})
    if not banner:
        raise HTTPException(status_code=404, detail="Banner not found")
    
    # Update banner with advanced scheduling
    schedule_update = {
        "scheduling": {
            "type": schedule_config.get("type", "one_time"),  # one_time, recurring
            "start_date": datetime.fromisoformat(schedule_config["start_date"]) if schedule_config.get("start_date") else None,
            "end_date": datetime.fromisoformat(schedule_config["end_date"]) if schedule_config.get("end_date") else None,
            "recurrence": schedule_config.get("recurrence"),  # daily, weekly, monthly
            "days_of_week": schedule_config.get("days_of_week", []),  # [1,2,3,4,5] for weekdays
            "time_of_day": schedule_config.get("time_of_day"),  # "09:00" format
            "target_timezones": schedule_config.get("target_timezones", ["UTC"])
        },
        "updated_at": datetime.utcnow()
    }
    
    await db.banners.update_one(
        {"banner_id": banner_id},
        {"$set": schedule_update}
    )
    
    # Create scheduled tasks (simplified - in production would use a job queue)
    if schedule_config.get("type") == "recurring":
        await _create_recurring_banner_schedule(banner_id, schedule_config)
    
    return {
        "message": "Banner scheduling updated successfully",
        "banner_id": banner_id,
        "scheduling": schedule_update["scheduling"]
    }

async def _create_recurring_banner_schedule(banner_id: str, config: Dict[str, Any]):
    """Create recurring schedule entries (simplified implementation)"""
    
    # In production, this would integrate with a job scheduler like Celery
    schedule_entries = []
    
    if config.get("recurrence") == "daily":
        # Create daily schedule entries for next 30 days
        for i in range(30):
            schedule_date = datetime.utcnow() + timedelta(days=i)
            schedule_entries.append({
                "schedule_id": str(uuid.uuid4()),
                "banner_id": banner_id,
                "scheduled_for": schedule_date,
                "status": "pending",
                "created_at": datetime.utcnow()
            })
    
    # Store schedule entries
    if schedule_entries:
        await db.banner_schedules.insert_many(schedule_entries)
    
    return len(schedule_entries)

# ===== EMAIL TEMPLATES MANAGEMENT =====

@router.post("/admin/email-templates")
async def create_email_template(
    name: str,
    subject: str,
    html_content: str,
    text_content: str,
    template_type: str,
    variables: List[str],
    current_user: UserProfile = Depends(require_role([UserRole.ADMIN, UserRole.SUPER_ADMIN]))
):
    """Create a new email template"""
    
    template_id = str(uuid.uuid4())
    
    template_doc = {
        "template_id": template_id,
        "name": name,
        "subject": subject,
        "html_content": html_content,
        "text_content": text_content,
        "template_type": template_type,
        "variables": variables,
        "is_active": True,
        "created_at": datetime.utcnow(),
        "last_modified": datetime.utcnow(),
        "created_by": current_user.user_id
    }
    
    await db.email_templates.insert_one(template_doc)
    
    # Remove ObjectId for response
    del template_doc["_id"]
    
    return template_doc

@router.get("/admin/email-templates")
async def get_email_templates(
    template_type: Optional[str] = Query(None),
    current_user: UserProfile = Depends(require_role([UserRole.ADMIN, UserRole.SUPER_ADMIN]))
):
    """Get all email templates"""
    
    query = {}
    if template_type:
        query["template_type"] = template_type
    
    templates = await db.email_templates.find(query).sort("created_at", -1).to_list(length=100)
    
    # Remove ObjectIds
    for template in templates:
        if "_id" in template:
            del template["_id"]
    
    return {
        "templates": templates,
        "total": len(templates)
    }

@router.put("/admin/email-templates/{template_id}")
async def update_email_template(
    template_id: str,
    updates: Dict[str, Any],
    current_user: UserProfile = Depends(require_role([UserRole.ADMIN, UserRole.SUPER_ADMIN]))
):
    """Update an email template"""
    
    # Add last modified timestamp
    updates["last_modified"] = datetime.utcnow()
    
    result = await db.email_templates.update_one(
        {"template_id": template_id},
        {"$set": updates}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Email template not found")
    
    # Return updated template
    template = await db.email_templates.find_one({"template_id": template_id})
    if template:
        del template["_id"]
    
    return template

# ===== API KEYS MANAGEMENT =====

@router.post("/admin/api-keys")
async def create_api_key(
    service_name: str,
    key_value: str,
    description: str,
    current_user: UserProfile = Depends(require_role([UserRole.SUPER_ADMIN]))  # Super admin only
):
    """Create a new API key configuration"""
    
    key_id = str(uuid.uuid4())
    
    key_doc = {
        "key_id": key_id,
        "service_name": service_name,
        "key_value": key_value,  # In production, this should be encrypted
        "description": description,
        "is_active": True,
        "created_at": datetime.utcnow(),
        "created_by": current_user.user_id,
        "last_used": None,
        "usage_count": 0
    }
    
    await db.api_keys.insert_one(key_doc)
    
    # Remove sensitive data and ObjectId for response
    response_data = key_doc.copy()
    response_data["key_value"] = "***HIDDEN***"  # Hide actual key value
    del response_data["_id"]
    
    return response_data

@router.get("/admin/api-keys")
async def get_api_keys(
    current_user: UserProfile = Depends(require_role([UserRole.SUPER_ADMIN]))
):
    """Get all API keys (super admin only)"""
    
    keys = await db.api_keys.find({}).sort("created_at", -1).to_list(length=100)
    
    # Remove sensitive data and ObjectIds
    for key in keys:
        key["key_value"] = "***HIDDEN***"
        if "_id" in key:
            del key["_id"]
    
    return {
        "api_keys": keys,
        "total": len(keys)
    }

@router.put("/admin/api-keys/{key_id}")
async def update_api_key(
    key_id: str,
    updates: Dict[str, Any],
    current_user: UserProfile = Depends(require_role([UserRole.SUPER_ADMIN]))
):
    """Update an API key configuration"""
    
    result = await db.api_keys.update_one(
        {"key_id": key_id},
        {"$set": updates}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="API key not found")
    
    return {"message": "API key updated successfully"}

@router.delete("/admin/api-keys/{key_id}")
async def delete_api_key(
    key_id: str,
    current_user: UserProfile = Depends(require_role([UserRole.SUPER_ADMIN]))
):
    """Delete an API key"""
    
    result = await db.api_keys.delete_one({"key_id": key_id})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="API key not found")
    
    return {"message": "API key deleted successfully"}

# ===== AUTOMATED WORKFLOWS =====

@router.post("/admin/workflows")
async def create_automated_workflow(
    name: str,
    description: str,
    trigger_event: str,
    steps: List[Dict[str, Any]],
    current_user: UserProfile = Depends(require_role([UserRole.ADMIN, UserRole.SUPER_ADMIN]))
):
    """Create a new automated workflow"""
    
    workflow_id = str(uuid.uuid4())
    
    # Convert steps to WorkflowStep objects
    workflow_steps = []
    for i, step in enumerate(steps):
        workflow_steps.append({
            "step_id": str(uuid.uuid4()),
            "step_type": step["step_type"],
            "config": step["config"],
            "order": i
        })
    
    workflow_doc = {
        "workflow_id": workflow_id,
        "name": name,
        "description": description,
        "trigger_event": trigger_event,
        "steps": workflow_steps,
        "is_active": True,
        "created_at": datetime.utcnow(),
        "created_by": current_user.user_id,
        "execution_count": 0,
        "last_executed": None
    }
    
    await db.automated_workflows.insert_one(workflow_doc)
    
    # Remove ObjectId for response
    del workflow_doc["_id"]
    
    return workflow_doc

@router.get("/admin/workflows")
async def get_automated_workflows(
    is_active: Optional[bool] = Query(None),
    current_user: UserProfile = Depends(require_role([UserRole.ADMIN, UserRole.SUPER_ADMIN]))
):
    """Get all automated workflows"""
    
    query = {}
    if is_active is not None:
        query["is_active"] = is_active
    
    workflows = await db.automated_workflows.find(query).sort("created_at", -1).to_list(length=100)
    
    # Remove ObjectIds
    for workflow in workflows:
        if "_id" in workflow:
            del workflow["_id"]
    
    return {
        "workflows": workflows,
        "total": len(workflows)
    }

@router.post("/admin/workflows/{workflow_id}/execute")
async def execute_workflow(
    workflow_id: str,
    context: Dict[str, Any],
    current_user: UserProfile = Depends(require_role([UserRole.ADMIN, UserRole.SUPER_ADMIN]))
):
    """Manually execute a workflow"""
    
    workflow = await db.automated_workflows.find_one({"workflow_id": workflow_id})
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    
    if not workflow["is_active"]:
        raise HTTPException(status_code=400, detail="Workflow is not active")
    
    # Execute workflow steps
    execution_results = []
    
    for step in sorted(workflow["steps"], key=lambda x: x["order"]):
        try:
            result = await _execute_workflow_step(step, context)
            execution_results.append({
                "step_id": step["step_id"],
                "step_type": step["step_type"],
                "status": "success",
                "result": result
            })
        except Exception as e:
            execution_results.append({
                "step_id": step["step_id"],
                "step_type": step["step_type"],
                "status": "error",
                "error": str(e)
            })
            break  # Stop execution on error
    
    # Update execution statistics
    await db.automated_workflows.update_one(
        {"workflow_id": workflow_id},
        {
            "$inc": {"execution_count": 1},
            "$set": {"last_executed": datetime.utcnow()}
        }
    )
    
    # Log execution
    await db.workflow_executions.insert_one({
        "execution_id": str(uuid.uuid4()),
        "workflow_id": workflow_id,
        "executed_by": current_user.user_id,
        "executed_at": datetime.utcnow(),
        "context": context,
        "results": execution_results,
        "status": "completed" if all(r["status"] == "success" for r in execution_results) else "failed"
    })
    
    return {
        "message": "Workflow executed",
        "workflow_id": workflow_id,
        "execution_results": execution_results
    }

async def _execute_workflow_step(step: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
    """Execute a single workflow step"""
    
    step_type = step["step_type"]
    config = step["config"]
    
    if step_type == "send_email":
        # Send email step
        template_id = config.get("template_id")
        recipient_criteria = config.get("recipient_criteria", {})
        
        # Get recipients based on criteria
        recipients = await db.users.find(recipient_criteria).to_list(length=10000)
        
        # In production, this would integrate with an email service
        return {
            "action": "email_sent",
            "recipients_count": len(recipients),
            "template_id": template_id
        }
    
    elif step_type == "apply_discount":
        # Apply discount step
        discount_id = config.get("discount_id")
        target_criteria = config.get("target_criteria", {})
        
        # Get target users
        users = await db.users.find(target_criteria).to_list(length=10000)
        applied_count = 0
        
        for user in users:
            # Check if user already has discount
            existing = await db.discount_usage.find_one({
                "user_id": user["user_id"],
                "discount_id": discount_id
            })
            
            if not existing:
                await db.discount_usage.insert_one({
                    "usage_id": str(uuid.uuid4()),
                    "discount_id": discount_id,
                    "user_id": user["user_id"],
                    "applied_at": datetime.utcnow(),
                    "application_reason": "Automated workflow",
                    "is_automated": True
                })
                applied_count += 1
        
        return {
            "action": "discount_applied",
            "applied_count": applied_count,
            "total_eligible": len(users)
        }
    
    elif step_type == "condition":
        # Conditional step
        condition_type = config.get("condition_type")
        condition_value = config.get("condition_value")
        
        # Simple condition evaluation (can be expanded)
        if condition_type == "user_count":
            user_count = await db.users.count_documents(config.get("user_criteria", {}))
            result = user_count >= condition_value
        else:
            result = True  # Default to true for unknown conditions
        
        return {
            "action": "condition_evaluated",
            "result": result,
            "condition_type": condition_type
        }
    
    elif step_type == "delay":
        # Delay step (in production, would be handled by job scheduler)
        delay_minutes = config.get("delay_minutes", 0)
        return {
            "action": "delay_scheduled",
            "delay_minutes": delay_minutes
        }
    
    else:
        raise Exception(f"Unknown step type: {step_type}")