import Link from 'next/link';
import { Navbar, Footer } from '@/components';

export default function Home() {
  return (
    <div className="min-h-screen flex flex-col">
      <Navbar />
      <main className="flex-grow container mx-auto p-4">
        <h1 className="text-3xl font-bold mb-4">IdeaForge</h1>
        <p className="mb-8">Validate ideas and generate MVPs instantly.</p>
        <div className="grid gap-4 sm:grid-cols-2">
          <Link href="/register" className="p-4 border rounded hover:bg-gray-100">Register</Link>
          <Link href="/login" className="p-4 border rounded hover:bg-gray-100">Login</Link>
          <Link href="/idea" className="p-4 border rounded hover:bg-gray-100">Submit Idea</Link>
          <Link href="/mvp" className="p-4 border rounded hover:bg-gray-100">Generate MVP</Link>
        </div>
      </main>
      <Footer />
    </div>
  );
}