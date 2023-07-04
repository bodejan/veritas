import {
  createStyles,
  Navbar,
  Code,
  Group,
  rem,
  Title,
} from '@mantine/core';
import React from 'react';
import NavigationItem from './NavigationItem';

// Define the styles for the component using Mantine's createStyles function
const useStyles = createStyles((theme) => ({
  navbar: {
    paddingTop: 0,
    height: "100vh",
    backgroundColor: theme.colors.gray[0]
  },

  section: {
    marginLeft: `calc(${theme.spacing.md} * -1)`,
    marginRight: `calc(${theme.spacing.md} * -1)`,
    marginBottom: theme.spacing.md,

    '&:not(:last-of-type)': {
      borderBottom: `${rem(1)} solid ${
        theme.colorScheme === 'dark' ? theme.colors.dark[4] : theme.colors.gray[3]
      }`,
    },
  },
}));

// Define the props for the Navigation component
interface NavigationItemProps {
  links: { icon: React.ElementType; label: string, link: string; }[];
}

// Navigation component
export default function Navigation({links}: NavigationItemProps) {
  const { classes, theme } = useStyles();

  return (
    <Navbar p="md" className={classes.navbar}  width={{ base: 250 }}>
      {/* Logo and Version section */}
      <Navbar.Section className={classes.section} p={10}>
        <Group position="apart">
          {/* Logo */}
          <Title order={1} color={theme.colors.dark[4]} sx={{ fontWeight: 700 }}>Heimdall</Title>
          {/* Version */}
          <Code sx={{ fontWeight: 700 }} color={theme.colors.gray[2]}>v1</Code>
        </Group>
      </Navbar.Section>

      {/* Navigation Links section */}
      <Navbar.Section className={classes.section}>
        <div>
          {/* Render navigation items */}
          {
            links.map((link, index) => (
              <NavigationItem link={link} key={index} />
            ))
          }
        </div>
      </Navbar.Section>
    </Navbar>
  );
}
