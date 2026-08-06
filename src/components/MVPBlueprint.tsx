import { useEffect, useState } from 'react';
import { api } from '@/utils/api';
import { motion } from 'framer-motion';

export default function MVPBlueprint({ blueprintId }: { blueprintId: string }) {
  const [features, setFeatures] = useState<any[]>([]);
  const [timeline, setTimeline] = useState<any>({});
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchBlueprint = async () => {
      try {
        const res = await api.get(`/api/blueprints/${blueprintId}`);
        setFeatures(res.data.features);
        setTimeline(res.data.timeline);
      } catch (err: any) {
        setError(err.response?.data?.detail || 'Failed to load blueprint');
      }
    };
    fetchBlueprint();
  }, [blueprintId]);

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
      <h3 className="text-lg font-semibold mb-2">MVP Blueprint</h3>
      <ul className="list-disc list-inside mb-4">
        {features.map((f, idx) => (
          <li key={idx}>{f.name}</li>
        ))}
      </ul>
      <h4 className="font-semibold">Timeline</h4>
      <pre className="bg-gray-100 dark:bg-gray-700 p-2 rounded overflow-x-auto">
        {JSON.stringify(timeline, null, 2)}
      </pre>
    </motion.div>
  );
}
