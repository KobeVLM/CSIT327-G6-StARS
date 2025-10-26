import { useState, useEffect } from 'react';
import { AppHeader } from './components/AppHeader';
import { Sidebar } from './components/Sidebar';
import { Login } from './components/pages/Login';
import { Register } from './components/pages/Register';
import { Dashboard } from './components/pages/Dashboard';
import { Profile } from './components/pages/Profile';
import { Settings } from './components/pages/Settings';

export default function App() {
  const [currentPage, setCurrentPage] = useState('login');
  const [currentUser, setCurrentUser] = useState<string | null>(null);
  const [fullName, setFullName] = useState<string>('');
  const [darkMode, setDarkMode] = useState(false);
  const [userStats] = useState({
    artworkCreated: 12,
    totalXP: 450,
    posts: 12,
    badges: 5,
  });
  const [userLevel] = useState(3);

  // Load dark mode preference from localStorage
  useEffect(() => {
    const savedDarkMode = localStorage.getItem('darkMode') === 'true';
    setDarkMode(savedDarkMode);
    if (savedDarkMode) {
      document.documentElement.classList.add('dark');
    }
  }, []);

  const handleLogin = (email: string) => {
    setCurrentUser(email);
    setFullName(email.split('@')[0]); // Use email username as name
    setCurrentPage('dashboard');
  };

  const handleRegister = (email: string, fullName: string) => {
    setCurrentUser(email);
    setFullName(fullName);
    setCurrentPage('dashboard');
  };

  const handleNavigate = (page: string) => {
    setCurrentPage(page);
  };

  const handleLogout = () => {
    setCurrentUser(null);
    setFullName('');
    setCurrentPage('login');
  };

  const handleToggleDarkMode = () => {
    const newDarkMode = !darkMode;
    setDarkMode(newDarkMode);
    localStorage.setItem('darkMode', String(newDarkMode));
    
    if (newDarkMode) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  };

  // Render auth pages
  if (!currentUser) {
    if (currentPage === 'register') {
      return (
        <Register 
          onRegister={handleRegister}
          onNavigateToLogin={() => setCurrentPage('login')}
        />
      );
    }
    return (
      <Login 
        onLogin={handleLogin}
        onNavigateToRegister={() => setCurrentPage('register')}
        onNavigateToAdminLogin={() => {}} // Remove admin login
      />
    );
  }

  // Render authenticated app
  return (
    <div className="h-screen flex flex-col">
      <AppHeader 
        user={{
          username: currentUser,
          level: userLevel,
          xp: userStats.totalXP,
        }}
        onNavigate={handleNavigate}
        onLogout={handleLogout}
      />
      
      <div className="flex-1 flex overflow-hidden">
        <Sidebar 
          currentPage={currentPage}
          onNavigate={handleNavigate}
          userStats={userStats}
        />
        
        <main className="flex-1 overflow-y-auto bg-background">
          {currentPage === 'dashboard' && (
            <Dashboard 
              username={currentUser} 
              fullName={fullName}
              onNavigate={handleNavigate}
              userStats={userStats}
            />
          )}
          {currentPage === 'profile' && <Profile username={currentUser} fullName={fullName} />}
          {currentPage === 'settings' && (
            <Settings 
              darkMode={darkMode}
              onToggleDarkMode={handleToggleDarkMode}
            />
          )}
        </main>
      </div>
    </div>
  );
}
