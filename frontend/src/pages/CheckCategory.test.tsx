
import '@testing-library/jest-dom/extend-expect'; 
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import CheckCategory from './CheckCategory';
import { MemoryRouter, useNavigate } from 'react-router-dom';
import userEvent from '@testing-library/user-event';

jest.mock('react-router-dom', () => ({
  ...jest.requireActual('react-router-dom'),
  useNavigate: jest.fn(),
}));

jest.mock('@mantine/notifications', () => ({
  notifications: {
    show: jest.fn(),
  },
}));

describe('CheckCategory', () => {
  test('renders the component', () => {
    render(
      <MemoryRouter>
        <CheckCategory setAppData={() => {}} />
      </MemoryRouter>
    );

    expect(screen.getByText(/Check privacy policies by app category/i)).toBeInTheDocument();
  });



  test('displays error message and does not submit form if category is not selected', () => {
    const setAppDataMock = jest.fn();

    render(
      <MemoryRouter>
        <CheckCategory setAppData={setAppDataMock} />
      </MemoryRouter>
    );

    

    const submitButton = screen.getByRole('button', { name: 'Check policies' });
    fireEvent.click(submitButton);

    expect(setAppDataMock).not.toHaveBeenCalled();
    expect(screen.getByText(/Please select a category/i)).toBeInTheDocument();
  });

  test('displays error message and does not submit form if number of apps is less than 1', () => {
    const setAppDataMock = jest.fn();

    render(
      <MemoryRouter>
        <CheckCategory setAppData={setAppDataMock} />
      </MemoryRouter>
    );

    const categorySelect = screen.getByLabelText('Select category');
    fireEvent.change(categorySelect, { target: { value: 'All' } });

    const numAppsInput = screen.getByLabelText('Amount of Apps');



    userEvent.type(numAppsInput, "0");

   

    const numAppsInput2 = screen.getByLabelText('Amount of Apps');


    const submitButton = screen.getByRole('button', { name: 'Check policies' });
    fireEvent.click(submitButton);

    expect(numAppsInput2).toBe(0)

  });



})
