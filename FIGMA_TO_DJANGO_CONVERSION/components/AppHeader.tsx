import { useState } from 'react';
import { Palette, Star, ChevronDown, Settings, LogOut } from 'lucide-react';
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
} from './ui/alert-dialog';

interface AppHeaderProps {
  user: {
    username: string;
    level: number;
    xp: number;
    profilePicture?: string;
  };
  onNavigate: (page: string) => void;
  onLogout: () => void;
}

export function AppHeader({ user, onNavigate, onLogout }: AppHeaderProps) {
  const xpProgress = (user.xp % 100) / 100 * 100;
  const [dropdownOpen, setDropdownOpen] = useState(false);
  const [showLogoutConfirm, setShowLogoutConfirm] = useState(false);

  return (
    <div className="bg-white border-b border-border px-6 py-3 flex items-center justify-between">
      <div className="flex items-center gap-3">
        <div className="bg-primary rounded-lg p-2">
          <Palette className="w-5 h-5 text-white" />
        </div>
        <div>
          <div style={{ fontSize: '1.125rem', fontWeight: '600' }}>Student Artist Space</div>
          <div style={{ fontSize: '0.75rem', color: 'var(--muted-foreground)' }}>
            Create • Share • Inspire
          </div>
        </div>
      </div>

      <div className="flex items-center gap-4">
        <div className="flex items-center gap-3">
          <div className="flex items-center gap-1.5 bg-yellow-50 px-3 py-1.5 rounded-lg">
            <Star className="w-4 h-4 text-yellow-500 fill-yellow-500" />
            <span style={{ fontSize: '0.875rem', fontWeight: '600' }}>Level {user.level}</span>
          </div>
          
          <div className="flex flex-col gap-1">
            <div className="w-32 bg-gray-200 rounded-full h-2 overflow-hidden">
              <div 
                className="bg-primary h-full rounded-full transition-all"
                style={{ width: `${xpProgress}%` }}
              />
            </div>
            <div style={{ fontSize: '0.625rem', color: 'var(--muted-foreground)' }}>
              {user.xp} XP
            </div>
          </div>
        </div>

        <div className="relative">
          <button
            onClick={() => setDropdownOpen(!dropdownOpen)}
            className="flex items-center gap-2 hover:bg-secondary/50 px-3 py-2 rounded-lg transition-colors"
          >
            <div className="w-10 h-10 rounded-full bg-primary/10 flex items-center justify-center overflow-hidden">
              {user.profilePicture ? (
                <img src={user.profilePicture} alt={user.username} className="w-full h-full object-cover" />
              ) : (
                <span className="text-primary" style={{ fontSize: '0.875rem', fontWeight: '600' }}>
                  {user.username.charAt(0).toUpperCase()}
                </span>
              )}
            </div>
            <span style={{ fontSize: '0.875rem', fontWeight: '500' }}>{user.username}</span>
            <ChevronDown className={`w-4 h-4 transition-transform ${dropdownOpen ? 'rotate-180' : ''}`} />
          </button>

          {dropdownOpen && (
            <>
              <div 
                className="fixed inset-0 z-10" 
                onClick={() => setDropdownOpen(false)}
              />
              <div className="absolute right-0 top-full mt-2 w-48 bg-white rounded-lg shadow-lg border border-border overflow-hidden z-20">
                <button
                  onClick={() => {
                    setDropdownOpen(false);
                    onNavigate('settings');
                  }}
                  className="w-full flex items-center gap-3 px-4 py-3 hover:bg-secondary transition-colors text-left"
                  style={{ fontSize: '0.875rem' }}
                >
                  <Settings className="w-4 h-4" />
                  <span>Settings</span>
                </button>
                <button
                  onClick={() => {
                    setDropdownOpen(false);
                    setShowLogoutConfirm(true);
                  }}
                  className="w-full flex items-center gap-3 px-4 py-3 hover:bg-secondary transition-colors text-left border-t border-border"
                  style={{ fontSize: '0.875rem' }}
                >
                  <LogOut className="w-4 h-4" />
                  <span>Logout</span>
                </button>
              </div>
            </>
          )}
        </div>
      </div>

      {/* Logout Confirmation Dialog */}
      <AlertDialog open={showLogoutConfirm} onOpenChange={setShowLogoutConfirm}>
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle>Confirm Logout</AlertDialogTitle>
            <AlertDialogDescription>
              Are you sure you want to log out? You will need to sign in again to access your account.
            </AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel>Cancel</AlertDialogCancel>
            <AlertDialogAction onClick={onLogout}>
              Logout
            </AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>
    </div>
  );
}
