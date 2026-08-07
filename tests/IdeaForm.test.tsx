import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { IdeaForm } from '../src/components/IdeaForm';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

const queryClient = new QueryClient();

const renderWithClient = (ui: React.ReactElement) =>
  render(<QueryClientProvider client={queryClient}>{ui}</QueryClientProvider>);

describe('IdeaForm', () => {
  test('validates required fields', async () => {
    renderWithClient(<IdeaForm />);
    fireEvent.click(screen.getByRole('button', { name: /validate idea/i }));
    expect(await screen.findByText(/description must be at least 10 characters/i)).toBeInTheDocument();
    expect(await screen.findByText(/select at least one tag/i)).toBeInTheDocument();
  });

  test('submits form with valid data', async () => {
    // Mock fetch
    global.fetch = jest.fn(() =>
      Promise.resolve({
        ok: true,
        json: () => Promise.resolve({
          ideaId: '123e4567-e89b-12d3-a456-426614174000',
          validationScore: 8.5,
          validationText: 'Good idea',
          recommendedFeatures: ['Feature A', 'Feature B'],
        }),
      })
    ) as jest.Mock;

    renderWithClient(<IdeaForm />);
    fireEvent.change(screen.getByLabelText(/idea description/i), {
      target: { value: 'This is a solid business idea for fintech.' },
    });
    fireEvent.change(screen.getByLabelText(/industry tags/i), {
      target: { value: 'fintech, healthtech' },
    });
    fireEvent.click(screen.getByRole('button', { name: /validate idea/i }));
    await waitFor(() => {
      expect(screen.getByRole('status')).toHaveTextContent(/validation successful/i);
    });
  });
});