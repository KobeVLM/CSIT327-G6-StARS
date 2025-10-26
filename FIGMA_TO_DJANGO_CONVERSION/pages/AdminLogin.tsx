import { useState } from 'react';
import { Header } from '../Header';
import { Shield, AlertCircle, Loader2 } from 'lucide-react';

interface AdminLoginProps {
  onAdminLogin: (email: string) => void;
  onNavigateToLogin: () => void;
}

export function AdminLogin({ onAdminLogin, onNavigateToLogin }: AdminLoginProps) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const validateEmail = (email: string) => {
    const emailRegex = /^[^\s@]+@gmail\.com$/;
    return emailRegex.test(email);
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    if (!email || !password) {
      setError('Please fill in all fields.');
      return;
    }

    if (!validateEmail(email)) {
      setError('Please enter a valid admin email (admin@gmail.com).');
      return;
    }

    setLoading(true);
    
    // Simulate API call - check for admin@gmail.com
    setTimeout(() => {
      if (email === 'admin@gmail.com' && password) {
        onAdminLogin(email);
      } else {
        setError('Invalid admin credentials.');
        setLoading(false);
      }
    }, 800);
  };

  return (
    <div className="min-h-screen flex flex-col">
      <Header showAuth={true} onLoginClick={onNavigateToLogin} />
      
      <div className="flex-1 flex items-center justify-center px-4" style={{ backgroundColor: '#F5F7FB' }}>
        <div className="w-full max-w-md">
          <div className="text-center mb-8">
            <div className="inline-flex items-center justify-center w-16 h-16 bg-primary rounded-full mb-4">
              <Shield className="w-8 h-8 text-white" />
            </div>
            <h1 style={{ fontSize: '1.75rem', fontWeight: '600', marginBottom: '0.5rem', color: '#2C3E50' }}>
              Admin Portal
            </h1>
            <p style={{ fontSize: '0.875rem', color: '#7C8AA0' }}>
              Access administrative controls and moderation tools
            </p>
          </div>

          <div className="bg-white rounded-lg p-8 shadow-sm">
            <h2 style={{ fontSize: '1.25rem', fontWeight: '600', marginBottom: '0.5rem' }}>
              Admin Sign In
            </h2>
            <p style={{ fontSize: '0.875rem', color: '#7C8AA0', marginBottom: '1.5rem' }}>
              Enter your admin credentials to continue
            </p>

            {error && (
              <div className="mb-4 p-3 bg-destructive/10 border border-destructive/20 rounded flex items-start gap-2">
                <AlertCircle className="w-4 h-4 text-destructive mt-0.5 flex-shrink-0" />
                <p style={{ fontSize: '0.875rem', color: 'var(--destructive)' }}>{error}</p>
              </div>
            )}

            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label 
                  htmlFor="email" 
                  className="block mb-1.5"
                  style={{ fontSize: '0.875rem', color: '#2C3E50' }}
                >
                  Admin Email:
                </label>
                <input
                  id="email"
                  type="email"
                  value={email}
                  onChange={(e) => {
                    setEmail(e.target.value);
                    setError('');
                  }}
                  placeholder="admin@gmail.com"
                  className="w-full px-3 py-2 border border-input rounded bg-white"
                  style={{ fontSize: '0.875rem' }}
                  disabled={loading}
                />
              </div>

              <div>
                <label 
                  htmlFor="password" 
                  className="block mb-1.5"
                  style={{ fontSize: '0.875rem', color: '#2C3E50' }}
                >
                  Password:
                </label>
                <input
                  id="password"
                  type="password"
                  value={password}
                  onChange={(e) => {
                    setPassword(e.target.value);
                    setError('');
                  }}
                  placeholder="Admin Password"
                  className="w-full px-3 py-2 border border-input rounded bg-white"
                  style={{ fontSize: '0.875rem' }}
                  disabled={loading}
                />
              </div>

              <button
                type="submit"
                className="w-full bg-primary text-white px-6 py-2.5 rounded hover:opacity-90 transition-opacity disabled:opacity-50 flex items-center justify-center gap-2"
                style={{ fontSize: '0.875rem', fontWeight: '500' }}
                disabled={loading}
              >
                {loading && <Loader2 className="w-4 h-4 animate-spin" />}
                {loading ? 'Authenticating...' : 'Admin Login'}
              </button>
            </form>

            <div className="mt-4 text-center">
              <button
                onClick={onNavigateToLogin}
                className="text-muted-foreground hover:text-primary transition-colors"
                style={{ fontSize: '0.875rem', fontWeight: '500' }}
              >
                ← Back to User Login
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
