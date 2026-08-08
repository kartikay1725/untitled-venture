import { useState } from 'react';
import { submitIdea } from '@/utils/api';

export default function IdeaForm() {
  const [description, setDescription] = useState('');
  const [score, setScore] = useState<number | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    try {
      const res = await submitIdea(description);
      setScore(res.validation_score);
    } catch (err: any) {
      setError(err.message || 'Submission failed');
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <textarea
        value={description}
        onChange={e => setDescription(e.target.value)}
        placeholder="Describe your idea"
        className="w-full border p-2 rounded"
        required
      />
      <button type="submit" className="px-4 py-2 bg-blue-600 text-white rounded">
        Validate Idea
      </button>
      {score !== null && <p>Validation Score: {score}</p>}
      {error && <p className="text-red-600">{error}</p>}
    </form>
  );
}