import { useForm } from 'react-hook-form';
import { z } from 'zod';
import { zodResolver } from '@hookform/resolvers/zod';
import { api } from '@/utils/api';
import { motion } from 'framer-motion';
import { useState } from 'react';

const schema = z.object({
  title: z.string().min(5, 'Title too short'),
  description: z.string().min(20, 'Description too short'),
});

type FormData = z.infer<typeof schema>;

export default function IdeaForm({ onSuccess }: { onSuccess: (id: string) => void }) {
  const { register, handleSubmit, formState: { errors, isSubmitting } } = useForm<FormData>({
    resolver: zodResolver(schema),
  });
  const [error, setError] = useState<string | null>(null);

  const onSubmit = async (data: FormData) => {
    try {
      const res = await api.post('/api/ideas', data);
      onSuccess(res.data.id);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Submission failed');
    }
  };

  return (
    <motion.form
      onSubmit={handleSubmit(onSubmit)}
      className="bg-white dark:bg-gray-800 p-6 rounded shadow"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
    >
      <h2 className="text-lg font-semibold mb-4">Submit Your Idea</h2>
      {error && <p className="text-red-600 mb-4">{error}</p>}
      <div className="mb-4">
        <label className="block text-sm font-medium mb-1">Title</label>
        <input
          {...register('title')}
          className="w-full border rounded p-2"
          aria-invalid={errors.title ? 'true' : 'false'}
          aria-describedby="title-error"
        />
        {errors.title && (
          <p id="title-error" className="text-red-600 text-sm">
            {errors.title.message}
          </p>
        )}
      </div>
      <div className="mb-4">
        <label className="block text-sm font-medium mb-1">Description</label>
        <textarea
          {...register('description')}
          className="w-full border rounded p-2"
          rows={5}
          aria-invalid={errors.description ? 'true' : 'false'}
          aria-describedby="description-error"
        />
        {errors.description && (
          <p id="description-error" className="text-red-600 text-sm">
            {errors.description.message}
          </p>
        )}
      </div>
      <button
        type="submit"
        disabled={isSubmitting}
        className="bg-primary hover:bg-primary-dark text-white px-4 py-2 rounded disabled:opacity-50"
      >
        {isSubmitting ? 'Submitting...' : 'Submit'}
      </button>
    </motion.form>
  );
}
