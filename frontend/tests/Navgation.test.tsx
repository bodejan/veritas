import "@testing-library/jest-dom";


import { render, screen } from '@testing-library/react';
import React from 'react'
import { MemoryRouter } from 'react-router-dom';
import Navigation from '../src/Components/Navigation';
import NavigationItem from '../src/Components/NavigationItem';
import { Check} from 'tabler-icons-react';


describe('Navigation', () => {


  const links = [
    { icon: Check, label: 'Home', link: '/home' },
    { icon: Check, label: 'About', link: '/about' },
    { icon: Check, label: 'Contact', link: '/contact' },
  ];

  it('renders navigation items', () => {
    render(
      <MemoryRouter>
        <Navigation links={links} />
      </MemoryRouter>
    );

    // Check if the navigation items are rendered correctly
    const navigationItems = screen.getAllByRole('link');
    expect(navigationItems).toHaveLength(links.length);

    links.forEach((link, index) => {
      expect(navigationItems[index]).toHaveTextContent(link.label);
      expect(navigationItems[index]).toHaveAttribute('href', link.link);
    });
  });
});

describe('NavigationItem', () => {
  const link = { icon: Check, label: 'Home', link: '/home' };

  it('renders link with correct label and icon', () => {
    render(
      <MemoryRouter>
        <NavigationItem link={link} />
      </MemoryRouter>
    );

    // Check if the link is rendered correctly
    const linkElement = screen.getByRole('link');
    expect(linkElement).toHaveTextContent(link.label);

    // You can also check if the icon is rendered correctly if you have access to the IconComponent
    // Replace 'IconComponent' with the actual component used for icons in your application
    // const iconElement = screen.getByTestId('icon'); // Assuming the icon has a test id
    // expect(iconElement).toBeInTheDocument();
  });

 

  // Add more test cases for different scenarios if needed
});

