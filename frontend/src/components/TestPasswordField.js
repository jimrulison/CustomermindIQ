import React, { useState } from 'react';
import { Eye, EyeOff } from 'lucide-react';

const TestPasswordField = () => {
    const [showPassword, setShowPassword] = useState(false);

    return (
        <div style={{ padding: '20px', background: 'white', margin: '10px' }}>
            <h3>Test Password Field with Eye Icons</h3>
            <div style={{ position: 'relative', display: 'inline-block' }}>
                <input
                    type={showPassword ? 'text' : 'password'}
                    value="testpassword"
                    readOnly
                    style={{
                        padding: '10px 40px 10px 10px',
                        border: '1px solid #ccc',
                        borderRadius: '4px',
                        width: '200px'
                    }}
                />
                <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    style={{
                        position: 'absolute',
                        right: '10px',
                        top: '50%',
                        transform: 'translateY(-50%)',
                        border: 'none',
                        background: 'transparent',
                        cursor: 'pointer',
                        color: '#666'
                    }}
                >
                    {showPassword ? <EyeOff size={20} /> : <Eye size={20} />}
                </button>
            </div>
            <p>Icon should appear here: {showPassword ? 'VISIBLE' : 'HIDDEN'}</p>
        </div>
    );
};

export default TestPasswordField;