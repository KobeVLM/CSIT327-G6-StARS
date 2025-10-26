import { useState } from 'react';
import { Bell, Globe, User, Lock, Moon, Sun } from 'lucide-react';

interface SettingsProps {
  darkMode: boolean;
  onToggleDarkMode: () => void;
}

export function Settings({ darkMode, onToggleDarkMode }: SettingsProps) {
  const [settings, setSettings] = useState({
    notificationsEnabled: true,
    emailNotifications: true,
    language: 'en',
    displayName: 'John Doe',
    email: 'john.doe@gmail.com',
    bio: 'Passionate digital artist exploring colors and creativity.',
  });

  const [saved, setSaved] = useState(false);
  const [showPasswordReset, setShowPasswordReset] = useState(false);

  const handleChange = (field: string, value: string | boolean) => {
    setSettings(prev => ({ ...prev, [field]: value }));
  };

  const handleSave = (e: React.FormEvent) => {
    e.preventDefault();
    setSaved(true);
    setTimeout(() => setSaved(false), 3000);
  };

  const handlePasswordReset = () => {
    setShowPasswordReset(true);
    setTimeout(() => setShowPasswordReset(false), 3000);
  };

  return (
    <div className="p-8 max-w-4xl">
      <div className="mb-6">
        <h1 style={{ fontSize: '1.75rem', fontWeight: '600', marginBottom: '0.5rem' }}>
          Settings
        </h1>
        <p style={{ fontSize: '0.875rem', color: '#7C8AA0' }}>
          Manage your account preferences and settings
        </p>
      </div>

      {saved && (
        <div className="bg-success/10 border border-success/20 rounded-lg px-4 py-3 mb-6">
          <p style={{ fontSize: '0.875rem', color: 'var(--success)' }}>Settings saved successfully!</p>
        </div>
      )}

      {showPasswordReset && (
        <div className="bg-primary/10 border border-primary/20 rounded-lg px-4 py-3 mb-6">
          <p style={{ fontSize: '0.875rem', color: 'var(--primary)' }}>Password reset email sent!</p>
        </div>
      )}

      <form onSubmit={handleSave} className="space-y-6">
        {/* Profile Settings */}
        <div className="bg-white rounded-lg p-6">
          <div className="flex items-center gap-3 mb-4">
            <div className="bg-primary/10 rounded-lg p-2">
              <User className="w-5 h-5 text-primary" />
            </div>
            <h2 style={{ fontSize: '1.25rem', fontWeight: '600' }}>Account Information</h2>
          </div>

          <div className="space-y-4">
            <div>
              <label htmlFor="displayName" className="block mb-2" style={{ fontSize: '0.875rem', fontWeight: '500' }}>
                Display Name
              </label>
              <input
                id="displayName"
                type="text"
                value={settings.displayName}
                onChange={(e) => handleChange('displayName', e.target.value)}
                className="w-full px-3 py-2 border border-input rounded bg-white"
                style={{ fontSize: '0.875rem' }}
              />
            </div>

            <div>
              <label htmlFor="email" className="block mb-2" style={{ fontSize: '0.875rem', fontWeight: '500' }}>
                Email Address
              </label>
              <input
                id="email"
                type="email"
                value={settings.email}
                onChange={(e) => handleChange('email', e.target.value)}
                className="w-full px-3 py-2 border border-input rounded bg-white"
                style={{ fontSize: '0.875rem' }}
              />
            </div>

            <div>
              <label htmlFor="bio" className="block mb-2" style={{ fontSize: '0.875rem', fontWeight: '500' }}>
                Bio
              </label>
              <textarea
                id="bio"
                value={settings.bio}
                onChange={(e) => handleChange('bio', e.target.value)}
                rows={3}
                className="w-full px-3 py-2 border border-input rounded bg-white resize-none"
                style={{ fontSize: '0.875rem' }}
              />
            </div>
          </div>
        </div>

        {/* Appearance Settings */}
        <div className="bg-white rounded-lg p-6">
          <div className="flex items-center gap-3 mb-4">
            <div className="bg-primary/10 rounded-lg p-2">
              {darkMode ? <Moon className="w-5 h-5 text-primary" /> : <Sun className="w-5 h-5 text-primary" />}
            </div>
            <h2 style={{ fontSize: '1.25rem', fontWeight: '600' }}>Appearance</h2>
          </div>

          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <div>
                <div style={{ fontSize: '0.875rem', fontWeight: '500', marginBottom: '0.25rem' }}>
                  Dark Mode
                </div>
                <div style={{ fontSize: '0.75rem', color: '#7C8AA0' }}>
                  Toggle between light and dark theme
                </div>
              </div>
              <label className="relative inline-flex items-center cursor-pointer">
                <input
                  type="checkbox"
                  checked={darkMode}
                  onChange={onToggleDarkMode}
                  className="sr-only peer"
                />
                <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-primary"></div>
              </label>
            </div>
          </div>
        </div>

        {/* Notification Settings */}
        <div className="bg-white rounded-lg p-6">
          <div className="flex items-center gap-3 mb-4">
            <div className="bg-primary/10 rounded-lg p-2">
              <Bell className="w-5 h-5 text-primary" />
            </div>
            <h2 style={{ fontSize: '1.25rem', fontWeight: '600' }}>Notifications</h2>
          </div>

          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <div>
                <div style={{ fontSize: '0.875rem', fontWeight: '500', marginBottom: '0.25rem' }}>
                  Enable Notifications
                </div>
                <div style={{ fontSize: '0.75rem', color: '#7C8AA0' }}>
                  Receive notifications about your artworks and activities
                </div>
              </div>
              <label className="relative inline-flex items-center cursor-pointer">
                <input
                  type="checkbox"
                  checked={settings.notificationsEnabled}
                  onChange={(e) => handleChange('notificationsEnabled', e.target.checked)}
                  className="sr-only peer"
                />
                <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-primary"></div>
              </label>
            </div>

            <div className="flex items-center justify-between">
              <div>
                <div style={{ fontSize: '0.875rem', fontWeight: '500', marginBottom: '0.25rem' }}>
                  Email Notifications
                </div>
                <div style={{ fontSize: '0.75rem', color: '#7C8AA0' }}>
                  Get updates and announcements via email
                </div>
              </div>
              <label className="relative inline-flex items-center cursor-pointer">
                <input
                  type="checkbox"
                  checked={settings.emailNotifications}
                  onChange={(e) => handleChange('emailNotifications', e.target.checked)}
                  className="sr-only peer"
                />
                <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-primary"></div>
              </label>
            </div>
          </div>
        </div>

        {/* Language Settings */}
        <div className="bg-white rounded-lg p-6">
          <div className="flex items-center gap-3 mb-4">
            <div className="bg-primary/10 rounded-lg p-2">
              <Globe className="w-5 h-5 text-primary" />
            </div>
            <h2 style={{ fontSize: '1.25rem', fontWeight: '600' }}>Language Preference</h2>
          </div>

          <div>
            <label htmlFor="language" className="block mb-2" style={{ fontSize: '0.875rem', fontWeight: '500' }}>
              Language
            </label>
            <select
              id="language"
              value={settings.language}
              onChange={(e) => handleChange('language', e.target.value)}
              className="w-full px-3 py-2 border border-input rounded bg-white"
              style={{ fontSize: '0.875rem' }}
            >
              <option value="en">English</option>
              <option value="es">Español</option>
              <option value="fr">Français</option>
              <option value="de">Deutsch</option>
              <option value="ja">日本語</option>
            </select>
          </div>
        </div>

        {/* Security Settings */}
        <div className="bg-white rounded-lg p-6">
          <div className="flex items-center gap-3 mb-4">
            <div className="bg-primary/10 rounded-lg p-2">
              <Lock className="w-5 h-5 text-primary" />
            </div>
            <h2 style={{ fontSize: '1.25rem', fontWeight: '600' }}>Security</h2>
          </div>

          <div>
            <div style={{ fontSize: '0.875rem', fontWeight: '500', marginBottom: '0.5rem' }}>
              Password Reset
            </div>
            <div style={{ fontSize: '0.75rem', color: '#7C8AA0', marginBottom: '1rem' }}>
              Request a password reset link via email
            </div>
            <button
              type="button"
              onClick={handlePasswordReset}
              className="bg-secondary text-foreground px-6 py-2.5 rounded hover:bg-secondary/80 transition-colors"
              style={{ fontSize: '0.875rem', fontWeight: '500' }}
            >
              Reset Password
            </button>
          </div>
        </div>

        {/* Save Button */}
        <div className="flex gap-3">
          <button
            type="submit"
            className="bg-primary text-white px-6 py-2.5 rounded hover:opacity-90 transition-opacity"
            style={{ fontSize: '0.875rem', fontWeight: '500' }}
          >
            Save Changes
          </button>
          <button
            type="button"
            onClick={() => window.history.back()}
            className="bg-white text-foreground border border-input px-6 py-2.5 rounded hover:bg-secondary transition-colors"
            style={{ fontSize: '0.875rem', fontWeight: '500' }}
          >
            Cancel
          </button>
        </div>
      </form>
    </div>
  );
}
