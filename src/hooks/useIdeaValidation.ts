import { useCallback } from 'react';
import { useMutation } from '@tanstack/react-query';
import { z } from 'zod';

const responseSchema = z.object({
  ideaId: z.string().uuid(),
  validationScore: z.number(),
  validationText: z.string(),
  recommendedFeatures: z.array(z.string()),
});

type IdeaPayload = {
  description: string;
  industry_tags: string[];
};

type IdeaResponse = z.infer<typeof responseSchema>;

export const useIdeaValidation = () => {
  const mutation = useMutation<IdeaResponse, Error, IdeaPayload>(
    async (payload) => {
      const res = await fetch('/api/ideas', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });
      if (!res.ok) {
        const err = await res.json();
        throw new Error(err.message || 'Validation failed');
      }
      const data = await res.json();
      return responseSchema.parse(data);
    },
    {
      onError: (err) => {
        console.error('Idea validation error:', err);
      },
    }
  );

  const mutateAsync = useCallback(
    async (payload: IdeaPayload) => {
      return mutation.mutateAsync(payload);
    },
    [mutation]
  );

  return {
    mutateAsync,
    isLoading: mutation.isLoading,
    error: mutation.error,
  };
};