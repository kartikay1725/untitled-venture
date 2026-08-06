import Link from 'next/link';
import { useAuth } from '@/hooks/useAuth';
import { motion } from 'framer-motion';

export default function Navbar() {
  const { user, logout } = useAuth();

  return (
    <nav className="flex items-center justify-between p-4 bg-primary text-white">
      <Link href="/" className="text-xl font-bold">
        MVPGenie
      </Link>
      <div className="flex items-center space-x-4">
        {user ? (
          <>
            <span>{user.email}</span>
            <button
              onClick={logout}
              className="bg-secondary hover:bg-secondary-dark text-white px-3 py-1 rounded"
            >
              Logout
            </button>
          </>
        ) : (
          <Link href="/login" className="bg-secondary hover:bg-secondary-dark text-white px-3 py-1 rounded">
            Login
          </Link>
        )}
      </div>
    </nav>
  );
}
