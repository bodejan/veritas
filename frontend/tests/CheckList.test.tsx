
import '@testing-library/jest-dom/extend-expect'; 
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import CheckList from '../src/pages/CheckList';
import { MemoryRouter, useNavigate } from 'react-router-dom';

jest.mock('react-router-dom', () => ({
  ...jest.requireActual('react-router-dom'),
  useNavigate: jest.fn(),
}));

describe('CheckList', () => {

  test('renders the component', () => {
    render(
      <MemoryRouter>
        <CheckList setAppData={() => {}} />
      </MemoryRouter>
    );

    expect(screen.getByText(/Check privacy policies by app list/i)).toBeInTheDocument();
  });



  /*
  test('handles empty app list', () => {
    const setAppDataMock = jest.fn();

    render(
      <MemoryRouter>
        <CheckList setAppData={setAppDataMock} />
      </MemoryRouter>
    );

    const checkButton = screen.getByText(/Check policies/i);
    fireEvent.click(checkButton);

    expect(screen.getByText(/Please upload a file or enter a list of apps/i)).toBeInTheDocument();
    expect(setAppDataMock).not.toHaveBeenCalled();
  });
  */
});
