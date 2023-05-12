import {
    createStyles,
    Navbar,
    Code,
    Group,
    rem,
    Title,
  } from '@mantine/core';

import NavigationItem from './NavigationItem';



  
  const useStyles = createStyles((theme) => ({
    navbar: {
      paddingTop: 0,
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
  

  
    mainLinks: {
      paddingLeft: `calc(${theme.spacing.md} - ${theme.spacing.xs})`,
      paddingRight: `calc(${theme.spacing.md} - ${theme.spacing.xs})`,
      paddingBottom: theme.spacing.md,
    },
  
    mainLink: {
      display: 'flex',
      alignItems: 'center',
      width: '100%',
      fontSize: theme.fontSizes.xs,
      padding: `${rem(8)} ${theme.spacing.xs}`,
      borderRadius: theme.radius.sm,
      fontWeight: 500,
      color: theme.colorScheme === 'dark' ? theme.colors.dark[0] : theme.colors.gray[7],
  
      '&:hover': {
        backgroundColor: theme.colorScheme === 'dark' ? theme.colors.dark[6] : theme.colors.gray[0],
        color: theme.colorScheme === 'dark' ? theme.white : theme.black,
      },
    },
  
    mainLinkInner: {
      display: 'flex',
      alignItems: 'center',
      flex: 1,
    },
  
    mainLinkIcon: {
      marginRight: theme.spacing.sm,
      color: theme.colorScheme === 'dark' ? theme.colors.dark[2] : theme.colors.gray[6],
    },


  }));
  

  interface NavigationItemProps {
    links: { icon: React.ElementType; label: string, link: string; }[];
  }

  export function Navigation({links}: NavigationItemProps) {
    const { classes, theme } = useStyles();

  
  
    return (
      <Navbar  p="md" className={classes.navbar}>
        <Navbar.Section className={classes.section} p={10}>
        <Group position="apart">
            <Title order={1} color={theme.colors.dark[4]} sx={{ fontWeight: 700 }}>Logo</Title>
            <Code sx={{ fontWeight: 700 }}>v1</Code>
        </Group>
        </Navbar.Section>
  
  
        <Navbar.Section className={classes.section}>
          <div className={classes.mainLinks}>
        {
          links.map((link) => (
                <NavigationItem link={link} />
            ))
        }
        </div>
        </Navbar.Section>
  

      </Navbar>
    );
  }