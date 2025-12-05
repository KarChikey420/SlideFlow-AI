import { useState } from 'react';
import { LoginPage } from './components/LoginPage';
import { SignupPage } from './components/SignupPage';
import { GeneratePPTPage } from './components/GeneratePPTPage';

type Page = 'login' | 'signup' | 'generate';

export default function App() {
  const [currentPage, setCurrentPage] = useState<Page>('login');
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [authToken, setAuthToken] = useState<string>('');

  const handleLogin = (token: string) => {
    setAuthToken(token);
    setIsAuthenticated(true);
    setCurrentPage('generate');
  };

  const handleSignup = () => {
    setCurrentPage('login');
  };

  const handleLogout = () => {
    setAuthToken('');
    setIsAuthenticated(false);
    setCurrentPage('login');
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-50 via-white to-purple-50">
      {currentPage === 'login' && (
        <LoginPage 
          onLogin={handleLogin}
          onSwitchToSignup={() => setCurrentPage('signup')}
        />
      )}
      {currentPage === 'signup' && (
        <SignupPage 
          onSignup={handleSignup}
          onSwitchToLogin={() => setCurrentPage('login')}
        />
      )}
      {currentPage === 'generate' && isAuthenticated && (
        <GeneratePPTPage onLogout={handleLogout} authToken={authToken} />
      )}
    </div>
  );
}
