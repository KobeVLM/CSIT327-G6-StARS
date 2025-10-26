import { useState } from 'react';
import { Header } from '../Header';
import { Palette, AlertCircle, Loader2 } from 'lucide-react';

interface RegisterProps {
  onRegister: (email: string, fullName: string) => void;
  onNavigateToLogin: () => void;
}

export function Register({ onRegister, onNavigateToLogin }: RegisterProps) {
  const [formData, setFormData] = useState({
    fullName: '',
    email: '',
    password: '',
    confirmPassword: '',
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const validateEmail = (email: string) => {
    const emailRegex = /^[^\s@]+@gmail\.com$/;
    return emailRegex.test(email);
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    if (!formData.fullName || !formData.email || !formData.password || !formData.confirmPassword) {
      setError('Please fill in all fields.');
      return;
    }

    if (!validateEmail(formData.email)) {
      setError('Please enter a valid email (user@gmail.com).');
      return;
    }

    if (formData.password !== formData.confirmPassword) {
      setError('Passwords do not match.');
      return;
    }

    if (formData.password.length < 6) {
      setError('Password must be at least 6 characters long.');
      return;
    }

    setLoading(true);

    // Simulate API call with email existence check
    setTimeout(() => {
      // For demo: check if email is 'existing@gmail.com'
      if (formData.email === 'existing@gmail.com') {
        setError('Email already exists.');
        setLoading(false);
      } else {
        onRegister(formData.email, formData.fullName);
      }
    }, 800);
  };

  const handleChange = (field: string, value: string) => {
    setFormData(prev => ({ ...prev, [field]: value }));
    setError('');
  };

  return (
    <div className="min-h-screen flex flex-col">
      <Header showAuth={true} onLoginClick={onNavigateToLogin} />
      
      <div className="flex-1 flex items-center justify-center px-4 py-8" style={{ backgroundColor: '#F5F7FB' }}>
        <div className="w-full max-w-md">
          <div className="text-center mb-8">
            <div className="inline-flex items-center justify-center w-16 h-16 bg-primary rounded-full mb-4">
              <Palette className="w-8 h-8 text-white" />
            </div>
            <h1 style={{ fontSize: '1.75rem', fontWeight: '600', marginBottom: '0.5rem', color: '#2C3E50' }}>
              Join the Community
            </h1>
            <p style={{ fontSize: '0.875rem', color: '#7C8AA0' }}>
              Create your account and start your artistic journey
            </p>
          </div>

          <div className="bg-white rounded-lg p-8 shadow-sm">
            <h2 style={{ fontSize: '1.25rem', fontWeight: '600', marginBottom: '0.5rem' }}>
              Create Account
            </h2>
            <p style={{ fontSize: '0.875rem', color: '#7C8AA0', marginBottom: '1.5rem' }}>
              Join thousands of student artists sharing their creativity
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
                  htmlFor="fullName" 
                  className="block mb-1.5"
                  style={{ fontSize: '0.875rem', color: '#2C3E50' }}
                >
                  Full Name:
                </label>
                <input
                  id="fullName"
                  type="text"
                  value={formData.fullName}
                  onChange={(e) => handleChange('fullName', e.target.value)}
                  placeholder="John Doe"
                  className="w-full px-3 py-2 border border-input rounded bg-white"
                  style={{ fontSize: '0.875rem' }}
                  disabled={loading}
                />
              </div>

              <div>
                <label 
                  htmlFor="email" 
                  className="block mb-1.5"
                  style={{ fontSize: '0.875rem', color: '#2C3E50' }}
                >
                  Email:
                </label>
                <input
                  id="email"
                  type="email"
                  value={formData.email}
                  onChange={(e) => handleChange('email', e.target.value)}
                  placeholder="user@gmail.com"
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
                  value={formData.password}
                  onChange={(e) => handleChange('password', e.target.value)}
                  placeholder="••••••••"
                  className="w-full px-3 py-2 border border-input rounded bg-white"
                  style={{ fontSize: '0.875rem' }}
                  disabled={loading}
                />
              </div>

              <div>
                <label 
                  htmlFor="confirmPassword" 
                  className="block mb-1.5"
                  style={{ fontSize: '0.875rem', color: '#2C3E50' }}
                >
                  Confirm Password:
                </label>
                <input
                  id="confirmPassword"
                  type="password"
                  value={formData.confirmPassword}
                  onChange={(e) => handleChange('confirmPassword', e.target.value)}
                  placeholder="••••••••"
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
                {loading ? 'Creating Account...' : 'Register'}
              </button>
            </form>

            <div className="mt-4 text-center">
              <span style={{ fontSize: '0.875rem', color: '#7C8AA0' }}>
                Already have an account?{' '}
              </span>
              <button
                onClick={onNavigateToLogin}
                className="text-primary hover:underline"
                style={{ fontSize: '0.875rem', fontWeight: '500' }}
              >
                Login here
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
