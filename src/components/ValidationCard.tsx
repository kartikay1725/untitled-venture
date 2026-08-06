import { useEffect, useState } from 'react';
import { api } from '@/utils/api';
import { motion } from 'framer-motion';

export default function ValidationCard({
  ideaId,
  onBlueprintGenerated,
}: {
  ideaId: string;
  onBlueprintGenerated: (id: string) => void;
}) {
  const [status, setStatus] = useState<'pending' | 'validating' | 'completed'>('pending');
  const [score, setScore] = useState<number | null>(null);
  const [feedback, setFeedback] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchValidation = async () => {
      setStatus('validating');
      try {
        const res = await api.get(`/api/ideas/${ideaId}/validation`);
        setScore(res.data.validation_score);
        setFeedback(res.data.validation_feedback);
        setStatus('completed');
        const blueprintRes = await api.post('/api/blueprints', {
          idea_id: ideaId,
          scope: 'basic',
        });
        onBlueprintGenerated(blueprintRes.data.id);
      } catch (err: any) {
        setError(err.response?.data?.detail || 'Validation failed');
        setStatus('completed');
      }
    };
    fetchValidation();
  }, [ideaId, onBlueprintGenerated]);

  if (status === 'validating') {
    return (
      <motion.div
        className="bg-white dark:bg-gray-800 p-6 rounded shadow"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
      >
        <p>Validating your idea...</p>
      </motion.div>
    );
  }

  if (error) {
    return (
      <motion.div
        className="bg-red-100 dark:bg-red-900 p-6 rounded shadow"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
      >
        <p className="text-red-600">{error}</p>
      </motion.div>
    );
  }

  return (
    <motion.div
      className="bg-white dark:bg-gray-800 p-6 rounded shadow"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
    >
      <h3 className="text-lg font-semibold mb-2">Validation Result</h3>
      <p>
        Score: <span className="font-mono">{score}</span>
      </p>
      <pre className="mt-2 bg-gray-100 dark:bg-gray-700 p-2 rounded overflow-x-auto">
        {JSON.stringify(feedback, null, 2)}
      </pre>
    </motion.div>
  );
}
