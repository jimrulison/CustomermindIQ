import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Alert, AlertDescription } from './ui/alert';
import { CheckCircle, XCircle, AlertTriangle, CreditCard, Shield, Users, Globe, Search, Database, Mail } from 'lucide-react';

const OverageApproval = ({ userEmail, onApprovalComplete }) => {
  const [pendingApprovals, setPendingApprovals] = useState([]);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [approvals, setApprovals] = useState({});
  const [totalCost, setTotalCost] = useState(0);

  useEffect(() => {
    loadOverageReview();
  }, [userEmail]);

  const loadOverageReview = async () => {
    try {
      const response = await fetch(
        `${process.env.REACT_APP_BACKEND_URL}/api/subscriptions/overage-review/${userEmail}`
      );
      const data = await response.json();
      
      if (data.status === 'success') {
        setPendingApprovals(data.pending_approvals || []);
        
        // Initialize approval state
        const initialApprovals = {};
        data.pending_approvals?.forEach(item => {
          initialApprovals[item.resource_type] = false;
        });
        setApprovals(initialApprovals);
      }
    } catch (error) {
      console.error('Failed to load overage review:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleApprovalChange = (resourceType, approved) => {
    setApprovals(prev => ({
      ...prev,
      [resourceType]: approved
    }));
    
    // Calculate total cost
    let total = 0;
    pendingApprovals.forEach(item => {
      const isApproved = resourceType === item.resource_type ? approved : approvals[item.resource_type];
      if (isApproved) {
        total += item.monthly_cost;
      }
    });
    setTotalCost(total);
  };

  const handleSubmitApprovals = async () => {
    setSubmitting(true);
    
    try {
      const approvedOverages = pendingApprovals
        .filter(item => approvals[item.resource_type])
        .map(item => ({
          resource_type: item.resource_type,
          overage_amount: item.overage_amount,
          monthly_cost: item.monthly_cost,
          approved: true
        }));

      const response = await fetch(
        `${process.env.REACT_APP_BACKEND_URL}/api/subscriptions/approve-overages`,
        {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            user_email: userEmail,
            approved_overages: approvedOverages
          })
        }
      );

      const data = await response.json();
      
      if (data.status === 'success') {
        if (onApprovalComplete) {
          onApprovalComplete(data);
        }
      } else {
        alert('Failed to process approvals: ' + (data.detail || 'Unknown error'));
      }
    } catch (error) {
      console.error('Failed to submit approvals:', error);
      alert('Failed to submit approvals. Please try again.');
    } finally {
      setSubmitting(false);
    }
  };

  const getResourceIcon = (resourceType) => {
    const icons = {
      contacts: Users,
      websites: Globe,
      keywords: Search,
      users: Users,
      api_calls_per_month: Database,
      email_sends_per_month: Mail,
      data_storage_gb: Database
    };
    const IconComponent = icons[resourceType] || AlertTriangle;
    return <IconComponent className="w-6 h-6" />;
  };

  if (loading) {
    return (
      <Card className="bg-slate-800 border-slate-700">
        <CardContent className="p-6">
          <div className="flex items-center justify-center">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
            <span className="ml-3 text-slate-300">Loading usage review...</span>
          </div>
        </CardContent>
      </Card>
    );
  }

  if (pendingApprovals.length === 0) {
    return (
      <Card className="bg-slate-800 border-slate-700">
        <CardContent className="p-6">
          <div className="flex items-center text-green-400">
            <CheckCircle className="w-6 h-6 mr-3" />
            <span>All usage within plan limits!</span>
          </div>
        </CardContent>
      </Card>
    );
  }

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      {/* Header */}
      <Card className="bg-slate-800 border-slate-700">
        <CardHeader>
          <CardTitle className="flex items-center text-orange-400">
            <AlertTriangle className="w-6 h-6 mr-2" />
            Approve Additional Services
          </CardTitle>
        </CardHeader>
        <CardContent>
          <Alert className="bg-orange-500/10 border-orange-500/20">
            <AlertTriangle className="h-4 w-4" />
            <AlertDescription className="text-orange-300">
              You've exceeded your plan limits. Review and approve additional services below to continue using them. 
              Unapproved items will be blocked until you upgrade your plan or approve the charges.
            </AlertDescription>
          </Alert>
        </CardContent>
      </Card>

      {/* Approval Items */}
      <div className="grid gap-4">
        {pendingApprovals.map((item) => (
          <Card key={item.resource_type} className="bg-slate-800 border-slate-700">
            <CardContent className="p-6">
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <div className="flex items-center mb-3">
                    <div className="text-blue-400 mr-3">
                      {getResourceIcon(item.resource_type)}
                    </div>
                    <div>
                      <h3 className="text-lg font-semibold text-white">{item.resource_name}</h3>
                      <p className="text-sm text-slate-400">{item.description}</p>
                    </div>
                  </div>
                  
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
                    <div className="bg-slate-700/30 rounded-lg p-3">
                      <div className="text-sm text-slate-400">Current Usage</div>
                      <div className="text-lg font-bold text-white">{item.current_usage.toLocaleString()}</div>
                    </div>
                    <div className="bg-slate-700/30 rounded-lg p-3">
                      <div className="text-sm text-slate-400">Plan Limit</div>
                      <div className="text-lg font-bold text-white">{item.plan_limit === 'Unlimited' ? 'Unlimited' : item.plan_limit.toLocaleString()}</div>
                    </div>
                    <div className="bg-slate-700/30 rounded-lg p-3">
                      <div className="text-sm text-slate-400">Overage Amount</div>
                      <div className="text-lg font-bold text-orange-400">+{item.overage_amount.toLocaleString()}</div>
                    </div>
                  </div>
                  
                  <div className="flex items-center justify-between">
                    <div className="text-sm text-slate-400">
                      Monthly cost: <span className="text-lg font-bold text-green-400">${item.monthly_cost.toFixed(2)}</span>
                    </div>
                    
                    <div className="flex items-center space-x-3">
                      <label className="flex items-center">
                        <input
                          type="checkbox"
                          checked={approvals[item.resource_type] || false}
                          onChange={(e) => handleApprovalChange(item.resource_type, e.target.checked)}
                          className="w-5 h-5 text-blue-600 bg-slate-700 border-slate-600 rounded focus:ring-blue-500"
                        />
                        <span className="ml-2 text-white font-medium">
                          {approvals[item.resource_type] ? 'Approved' : 'Approve'}
                        </span>
                      </label>
                      
                      {approvals[item.resource_type] ? (
                        <CheckCircle className="w-5 h-5 text-green-400" />
                      ) : (
                        <XCircle className="w-5 h-5 text-red-400" />
                      )}
                    </div>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Summary & Submit */}
      <Card className="bg-slate-800 border-slate-700">
        <CardContent className="p-6">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center">
              <CreditCard className="w-6 h-6 text-green-400 mr-3" />
              <div>
                <h3 className="text-lg font-semibold text-white">Monthly Billing Summary</h3>
                <p className="text-sm text-slate-400">Additional monthly charges for approved services</p>
              </div>
            </div>
            <div className="text-right">
              <div className="text-sm text-slate-400">Additional Monthly Cost:</div>
              <div className="text-2xl font-bold text-green-400">${totalCost.toFixed(2)}</div>
            </div>
          </div>
          
          <div className="flex items-center justify-between p-4 bg-slate-700/30 rounded-lg mb-4">
            <div className="flex items-center text-blue-400">
              <Shield className="w-5 h-5 mr-2" />
              <span className="text-sm">
                You'll receive an email notification 24 hours before billing with a detailed breakdown.
              </span>
            </div>
          </div>
          
          <div className="flex gap-3">
            <Button
              onClick={handleSubmitApprovals}
              disabled={submitting || Object.values(approvals).every(v => !v)}
              className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2"
            >
              {submitting ? 'Processing...' : `Approve Selected Services (${Object.values(approvals).filter(Boolean).length})`}
            </Button>
            
            <Button
              variant="outline"
              onClick={() => window.location.reload()}
              className="border-slate-600 text-slate-300 hover:bg-slate-700"
            >
              Cancel & Block All
            </Button>
          </div>
          
          <div className="mt-4 text-xs text-slate-400">
            <p>• Approved services will be available immediately</p>
            <p>• You can modify or cancel approvals anytime from your account settings</p>
            <p>• Billing occurs monthly on your regular billing date</p>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default OverageApproval;