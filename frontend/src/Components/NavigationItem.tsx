import { UnstyledButton, createStyles, rem } from '@mantine/core';
import React from 'react';
import { useLocation, Link } from 'react-router-dom';

// Define the component's styles using Mantine's createStyles function
const useStyles = createStyles((theme) => ({
  // Styling for the main link element
  mainLink: {
    display: 'flex',
    alignItems: 'center',
    width: '100%',
    fontSize: theme.fontSizes.sm,
    padding: `${rem(8)} ${theme.spacing.xs}`,
    fontWeight: 500,
    color: theme.colorScheme === 'dark' ? theme.colors.dark[0] : theme.colors.gray[7],
    '&:hover': {
      backgroundColor: theme.colors.gray[2],
      fontWeight: 700,
      color: theme.colorScheme === 'dark' ? theme.white : theme.black,
    },
  },
  // Styling for the inner container of the main link element
  mainLinkInner: {
    display: 'flex',
    alignItems: 'center',
    flex: 1,
  },
  // Styling for the icon within the main link element
  mainLinkIcon: {
    marginRight: theme.spacing.sm,
    color: theme.colorScheme === 'dark' ? theme.colors.dark[2] : theme.colors.gray[6],
  },
}));

// Define the prop types for the NavigationItem component
interface NavigationItemProps {
  link: { icon: React.ElementType; label: string; link: string };
}

// NavigationItem component
export default function NavigationItem({ link }: NavigationItemProps) {
  // Retrieve the styles and theme using the useStyles hook
  const { classes, theme } = useStyles();
  // Access the current location using the useLocation hook from react-router-dom
  const location = useLocation();
  // Determine if the current link is active based on the location's pathname
  const isActive = location.pathname.includes(link.link);

  return (
    // Render the link element provided by react-router-dom
    <Link to={link.link} style={{ textDecoration: 'none' }}>
      {/* Render the main link element */}
      <UnstyledButton
        key={link.label}
        className={classes.mainLink}
        // Apply dynamic styling to the main link if it is active
        sx={isActive ? { backgroundColor: theme.colors.gray[2], fontWeight: 700 } : {}}
      >
        {/* Render the inner container of the main link */}
        <div className={classes.mainLinkInner}>
          {/* Render the icon for the link */}
          <link.icon size={20} className={classes.mainLinkIcon} />
          {/* Render the label for the link */}
          <span>{link.label}</span>
        </div>
      </UnstyledButton>
    </Link>
  );
}
