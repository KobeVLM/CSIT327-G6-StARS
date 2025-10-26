import { Home, Search, Upload, User, Shield } from 'lucide-react';

interface SidebarProps {
  currentPage: string;
  onNavigate: (page: string) => void;
  userStats: {
    artworkCreated: number;
    totalXP: number;
  };
  isAdmin?: boolean;
}

export function Sidebar({ currentPage, onNavigate, userStats, isAdmin = false }: SidebarProps) {
  const menuItems = [
    { id: 'dashboard', label: 'Home', icon: Home },
    { id: 'browse', label: 'Browse', icon: Search },
    { id: 'upload', label: 'Upload Artwork', icon: Upload },
    { id: 'profile', label: 'Profile', icon: User },
  ];

  // Add admin-only sections
  const adminMenuItems = isAdmin ? [
    { id: 'moderation', label: 'Moderation', icon: Shield },
  ] : [];

  return (
    <div className="w-64 bg-white border-r border-border h-full flex flex-col">
      <nav className="p-4 flex-1">
        {menuItems.map((item) => {
          const Icon = item.icon;
          const isActive = currentPage === item.id;
          return (
            <button
              key={item.id}
              onClick={() => onNavigate(item.id)}
              className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg mb-2 transition-colors ${
                isActive 
                  ? 'bg-secondary text-primary' 
                  : 'text-muted-foreground hover:bg-secondary/50'
              }`}
              style={{ fontSize: '0.875rem' }}
            >
              <Icon className="w-5 h-5" />
              <span>{item.label}</span>
            </button>
          );
        })}

        {isAdmin && adminMenuItems.length > 0 && (
          <>
            <div className="my-4 border-t border-border" />
            <div style={{ fontSize: '0.75rem', color: 'var(--muted-foreground)', marginBottom: '0.5rem', paddingLeft: '1rem' }}>
              Admin
            </div>
            {adminMenuItems.map((item) => {
              const Icon = item.icon;
              const isActive = currentPage === item.id;
              return (
                <button
                  key={item.id}
                  onClick={() => onNavigate(item.id)}
                  className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg mb-2 transition-colors ${
                    isActive 
                      ? 'bg-secondary text-primary' 
                      : 'text-muted-foreground hover:bg-secondary/50'
                  }`}
                  style={{ fontSize: '0.875rem' }}
                >
                  <Icon className="w-5 h-5" />
                  <span>{item.label}</span>
                </button>
              );
            })}
          </>
        )}
      </nav>

      <div className="p-4 border-t border-border">
        <div style={{ fontSize: '0.75rem', color: 'var(--muted-foreground)', marginBottom: '0.5rem' }}>
          Quick Stats
        </div>
        <div className="space-y-2">
          <div className="flex justify-between items-center">
            <span style={{ fontSize: '0.875rem' }}>Artwork Created</span>
            <span style={{ fontSize: '0.875rem', fontWeight: '600' }}>{userStats.artworkCreated}</span>
          </div>
          <div className="flex justify-between items-center">
            <span style={{ fontSize: '0.875rem' }}>Total XP</span>
            <span style={{ fontSize: '0.875rem', fontWeight: '600' }}>{userStats.totalXP}</span>
          </div>
        </div>
      </div>
    </div>
  );
}
