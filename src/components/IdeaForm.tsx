import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { useIdeaValidation } from '../hooks/useIdeaValidation';
import { Spinner } from './LoadingSpinner';

const schema = z.object({
  description: z.string().min(10, 'Description must be at least 10 characters'),
  industry_tags: z.array(z.string().min(1)).min(1, 'Select at least one tag'),
});

type FormValues = z.infer<typeof schema>;

export const IdeaForm: React.FC = () => {
  const [submitted, setSubmitted] = useState(false);
  const { register, handleSubmit, formState: { errors } } = useForm<FormValues>({
    resolver: zodResolver(schema),
  });
  const { mutateAsync, isLoading, error } = useIdeaValidation();

  const onSubmit = async (data: FormValues) => {
    try {
      await mutateAsync({
        description: data.description,
        industry_tags: data.industry_tags,
      });
      setSubmitted(true);
    } catch (e) {
      // error handled by hook
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: 20 }}
      transition={{ duration: 0.3, ease: 'easeInOut' }}
      className="max-w-2xl mx-auto p-8 bg-var(--color-surface) rounded-xl shadow-md"
    >
      <h2 className="text-2xl font-semibold mb-6 text-var(--color-text)" >Submit Your Business Idea</h2>
      <form onSubmit={handleSubmit(onSubmit)} noValidate>
        <div className="mb-4">
          <label htmlFor="description" className="block text-sm font-medium mb-1 text-var(--color-text)" >Idea Description</label>
          <textarea
            id="description"
            {...register('description')}
            className="w-full border border-var(--color-border) rounded p-2 focus:outline-none focus:ring-2 focus:ring-var(--color-primary)"
            rows={4}
            aria-invalid={errors.description ? 'true' : 'false'}
            aria-describedby="description-error"
          />
          {errors.description && (
            <p id="description-error" className="text-sm text-var(--color-error) mt-1">
              {errors.description.message}
            </p>
          )}
        </div>
        <div className="mb-4">
          <label htmlFor="industry_tags" className="block text-sm font-medium mb-1 text-var(--color-text)" >Industry Tags</label>
          <input
            id="industry_tags"
            type="text"
            placeholder="e.g. fintech, healthtech"
            {...register('industry_tags')}
            className="w-full border border-var(--color-border) rounded p-2 focus:outline-none focus:ring-2 focus:ring-var(--color-primary)"
            aria-invalid={errors.industry_tags ? 'true' : 'false'}
            aria-describedby="industry_tags-error"
          />
          {errors.industry_tags && (
            <p id="industry_tags-error" className="text-sm text-var(--color-error) mt-1">
              {errors.industry_tags.message}
            </p>
          )}
        </div>
        <button
          type="submit"
          disabled={isLoading}
          className="w-full py-2 px-4 bg-var(--color-primary) text-white rounded hover:scale-102 transition-transform duration-200 ease-in-out"
        >
          {isLoading ? <Spinner /> : 'Validate Idea'}
        </button>
        {error && (
          <p className="mt-4 text-sm text-var(--color-error)" role="alert">
            {error.message}
          </p>
        )}
        {submitted && (
          <p className="mt-4 text-sm text-var(--color-success)" role="status">
            Validation successful! Check your email for the score.
          </p>
        )}
      </form>
    </motion.div>
  );
};