import React, { useState, useEffect } from 'react';
import { GoogleOAuthProvider, GoogleLogin } from '@react-oauth/google';

const Dashboard = () => {
    const [companyId, setCompanyId] = useState(null);
    const [companyName, setCompanyName] = useState('');

    const [activeTab, setActiveTab] = useState('leads');
    const [leads, setLeads] = useState([]);
    // State now uses 'name' to match the merged database model
    const [settings, setSettings] = useState({ name: '', report_email: '', urgency_threshold: 0, is_active: true, phone: '', address: '' });
    const [loading, setLoading] = useState(false);
    const [message, setMessage] = useState('');

    const GOOGLE_CLIENT_ID = import.meta.env.VITE_GOOGLE_CLIENT_ID;

    const [isSignUp, setIsSignUp] = useState(false);
    const [newCompanyName, setNewCompanyName] = useState('');

    const handleGoogleSuccess = async (credentialResponse) => {
        try {
            const response = await fetch("http://localhost:8000/auth/google", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ token: credentialResponse.credential })
            });

            const data = await response.json();

            if (response.ok) {
                setCompanyId(data.company_id);
                setCompanyName(data.company_name);
            } else {
                alert(data.detail);
            }
        } catch (error) {
            console.error("Auth error:", error);
        }
    };

    const handleGoogleSignUp = async (credentialResponse) => {
        if (!newCompanyName.trim()) {
            alert("Please enter a company name first.");
            return;
        }

        try {
            const response = await fetch("http://localhost:8000/auth/signup", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    token: credentialResponse.credential,
                    company_name: newCompanyName
                })
            });

            const data = await response.json();

            if (response.ok) {
                setCompanyId(data.company_id);
                setCompanyName(data.company_name);
            } else {
                alert(data.detail);
            }
        } catch (error) {
            console.error("Signup error:", error);
        }
    };

    const handleLogout = () => {
        setCompanyId(null);
        setCompanyName('');
        setLeads([]);
    };

    useEffect(() => {
        if (!companyId) return;

        if (activeTab === 'leads') {
            fetchLeads();
        } else {
            fetchSettings();
        }
    }, [activeTab, companyId]);

    const fetchLeads = async () => {
        setLoading(true);
        try {
            const response = await fetch(`http://localhost:8000/leads/company/${companyId}`);
            const data = await response.json();
            setLeads(data);
        } catch (error) {
            console.error("Error fetching leads:", error);
        }
        setLoading(false);
    };

    const fetchSettings = async () => {
        setLoading(true);
        try {
            // URL updated to the consolidated companies endpoint
            const response = await fetch(`http://localhost:8000/companies/${companyId}`);
            if (response.ok) {
                const data = await response.json();
                setSettings(data);
            }
        } catch (error) {
            console.error("Error fetching settings:", error);
        }
        setLoading(false);
    };

    const handleSettingsSave = async (e) => {
        e.preventDefault();
        setMessage('Saving...');
        try {
            // URL updated to the consolidated companies endpoint
            const response = await fetch(`http://localhost:8000/companies/${companyId}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(settings)
            });

            if (response.ok) {
                setMessage('Settings saved successfully!');
                setTimeout(() => setMessage(''), 3000);
            } else {
                setMessage('Failed to save settings.');
            }
        } catch (error) {
            setMessage('Error connecting to server.');
        }
    };

    if (!companyId) {
        return (
            <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', height: '100vh', fontFamily: 'sans-serif', backgroundColor: '#f4f7f6' }}>
                <div style={{ background: 'white', padding: '40px', borderRadius: '8px', boxShadow: '0 4px 6px rgba(0,0,0,0.1)', textAlign: 'center', maxWidth: '400px', width: '100%' }}>

                    <h2 style={{ marginTop: 0 }}>Bulkhead Bot</h2>
                    <p style={{ color: '#666', marginBottom: '20px' }}>
                        {isSignUp ? "Create your command center account." : "Log in to view your leads."}
                    </p>

                    {isSignUp && (
                        <input
                            type="text"
                            placeholder="Enter your Company Name"
                            value={newCompanyName}
                            onChange={(e) => setNewCompanyName(e.target.value)}
                            style={{ width: '100%', padding: '10px', marginBottom: '20px', border: '1px solid #ccc', borderRadius: '4px', boxSizing: 'border-box' }}
                        />
                    )}

                    <GoogleOAuthProvider clientId={GOOGLE_CLIENT_ID}>
                        <GoogleLogin
                            onSuccess={isSignUp ? handleGoogleSignUp : handleGoogleSuccess}
                            onError={() => console.log('Google Auth Failed')}
                        />
                    </GoogleOAuthProvider>

                    <div style={{ marginTop: '20px', fontSize: '14px' }}>
                        {isSignUp ? (
                            <p>Already have an account? <span onClick={() => setIsSignUp(false)} style={{ color: '#007bff', cursor: 'pointer', textDecoration: 'underline' }}>Log In</span></p>
                        ) : (
                            <p>Don't have an account? <span onClick={() => setIsSignUp(true)} style={{ color: '#007bff', cursor: 'pointer', textDecoration: 'underline' }}>Sign Up</span></p>
                        )}
                    </div>

                </div>
            </div>
        );
    }

    return (
        <div style={{ padding: '20px', fontFamily: 'sans-serif', maxWidth: '1200px', margin: '0 auto' }}>

            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', borderBottom: '2px solid #eee', paddingBottom: '10px', marginBottom: '20px' }}>
                <h1 style={{ margin: 0 }}>
                    {companyName ? `${companyName} Dashboard` : 'Company Dashboard'}
                </h1>
                <button
                    onClick={handleLogout}
                    style={{ padding: '8px 16px', background: '#dc3545', color: '#fff', border: 'none', borderRadius: '4px', cursor: 'pointer', fontWeight: 'bold' }}
                >
                    Log Out
                </button>
            </div>

            {/* Navigation Tabs */}
            <div style={{ marginBottom: '20px', display: 'flex', gap: '10px' }}>
                <button
                    onClick={() => setActiveTab('leads')}
                    style={{ padding: '10px 20px', cursor: 'pointer', background: activeTab === 'leads' ? '#007bff' : '#eee', color: activeTab === 'leads' ? '#fff' : '#000', border: 'none', borderRadius: '4px' }}
                >
                    View Leads
                </button>
                <button
                    onClick={() => setActiveTab('settings')}
                    style={{ padding: '10px 20px', cursor: 'pointer', background: activeTab === 'settings' ? '#007bff' : '#eee', color: activeTab === 'settings' ? '#fff' : '#000', border: 'none', borderRadius: '4px' }}
                >
                    Bot Settings
                </button>
            </div>

            {loading && <p>Loading data...</p>}

            {/* TAB 1: LEADS TABLE */}
            {activeTab === 'leads' && !loading && (
                <div>
                    <h2>Recent Leads</h2>
                    <table style={{ width: '100%', borderCollapse: 'collapse', marginTop: '10px' }}>
                        <thead>
                            <tr style={{ background: '#f8f9fa', textAlign: 'left' }}>
                                <th style={thStyle}>Date</th>
                                <th style={thStyle}>Name</th>
                                <th style={thStyle}>Phone</th>
                                <th style={thStyle}>Project</th>
                                <th style={thStyle}>Size (ft)</th>
                                <th style={thStyle}>Timeline</th>
                                <th style={thStyle}>Urgency (Months)</th>
                                <th style={thStyle}>Notes</th>
                            </tr>
                        </thead>
                        <tbody>
                            {leads.map(lead => (
                                <tr key={lead.id} style={{ borderBottom: '1px solid #eee' }}>
                                    <td style={tdStyle}>{new Date(lead.created_at).toLocaleDateString()}</td>
                                    <td style={tdStyle}>{lead.name}</td>
                                    <td style={tdStyle}>{lead.phone}</td>
                                    <td style={tdStyle}>{lead.project_type || 'N/A'}</td>
                                    <td style={tdStyle}>{lead.linear_feet || 'N/A'}</td>
                                    <td style={tdStyle}>{lead.timeline || 'N/A'}</td>
                                    <td style={tdStyle}>
                                        {lead.timeline_parsed !== null ? lead.timeline_parsed : 'N/A'}
                                    </td>
                                    <td style={tdStyle}>{lead.notes || 'N/A'}</td>
                                </tr>
                            ))}
                            {leads.length === 0 && (
                                <tr>
                                    <td colSpan="8" style={{ textAlign: 'center', padding: '20px' }}>No leads found.</td>
                                </tr>
                            )}
                        </tbody>
                    </table>
                </div>
            )}

            {/* TAB 2: SETTINGS FORM */}
            {activeTab === 'settings' && !loading && (
                <div style={{ maxWidth: '600px' }}>
                    <h2>Bot Settings</h2>
                    <form onSubmit={handleSettingsSave} style={{ display: 'flex', flexDirection: 'column', gap: '15px' }}>

                        <div>
                            <label style={labelStyle}>Company Name</label>
                            <input
                                type="text"
                                value={settings.name || ''}
                                onChange={(e) => setSettings({ ...settings, name: e.target.value })}
                                style={inputStyle}
                            />
                        </div>

                        <div>
                            <label style={labelStyle}>Reporting Email (Where leads are sent)</label>
                            <input
                                type="email"
                                value={settings.report_email || ''}
                                onChange={(e) => setSettings({ ...settings, report_email: e.target.value })}
                                style={inputStyle}
                            />
                        </div>

                        <div>
                            <label style={labelStyle}>Phone Number</label>
                            <input
                                type="text"
                                value={settings.phone || ''}
                                onChange={(e) => setSettings({ ...settings, phone: e.target.value })}
                                style={inputStyle}
                            />
                        </div>

                        <div>
                            <label style={labelStyle}>Company Address</label>
                            <input
                                type="text"
                                value={settings.address || ''}
                                onChange={(e) => setSettings({ ...settings, address: e.target.value })}
                                style={inputStyle}
                            />
                        </div>

                        <div>
                            <label style={labelStyle}>Urgency Threshold (Months - triggers immediate alert)</label>
                            <input
                                type="number"
                                step="0.1"
                                value={settings.urgency_threshold || 0}
                                onChange={(e) => setSettings({ ...settings, urgency_threshold: parseFloat(e.target.value) })}
                                style={inputStyle}
                            />
                        </div>

                        <div>
                            <label style={{ display: 'flex', alignItems: 'center', gap: '10px', fontWeight: 'bold' }}>
                                <input
                                    type="checkbox"
                                    checked={settings.is_active || false}
                                    onChange={(e) => setSettings({ ...settings, is_active: e.target.checked })}
                                />
                                Bot is Active on Website
                            </label>
                        </div>

                        <button type="submit" style={{ padding: '10px 20px', background: '#28a745', color: '#fff', border: 'none', borderRadius: '4px', cursor: 'pointer', fontSize: '16px' }}>
                            Save Settings
                        </button>

                        {message && <p style={{ color: message.includes('Error') || message.includes('Failed') ? 'red' : 'green', fontWeight: 'bold' }}>{message}</p>}
                    </form>
                </div>
            )}
        </div>
    );
};

const thStyle = { padding: '12px', borderBottom: '2px solid #ddd' };
const tdStyle = { padding: '12px' };
const labelStyle = { display: 'block', fontWeight: 'bold', marginBottom: '5px' };
const inputStyle = { width: '100%', padding: '10px', border: '1px solid #ccc', borderRadius: '4px' };

export default Dashboard;