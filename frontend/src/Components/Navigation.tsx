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
            <Code sx={{ fontWeight: 700 }} color="dark">v1</Code>
        </Group>
        </Navbar.Section>
  
  
        <Navbar.Section className={classes.section}>
          <div>
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