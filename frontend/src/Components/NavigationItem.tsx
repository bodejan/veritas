import { UnstyledButton, createStyles, rem } from '@mantine/core'
import React from 'react'
import {useLocation, Link } from 'react-router-dom';
  
const useStyles = createStyles((theme) => ({
    mainLink: {
      display: 'flex',
      alignItems: 'center',
      width: '100%',
      fontSize: theme.fontSizes.xs,
      padding: `${rem(8)} ${theme.spacing.xs}`,

      fontWeight: 500,
      color: theme.colorScheme === 'dark' ? theme.colors.dark[0] : theme.colors.gray[7],
      
  
      '&:hover': {
        backgroundColor: theme.colors.gray[2],
        fontWeight: 700,
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
    link: { icon: React.ElementType; label: string, link: string; };
  }

export default function NavigationItem({link}: NavigationItemProps) {
    const { classes, theme } = useStyles();
    const location = useLocation();
    const isActive = location.pathname.includes(link.link);

  return (
   
        <Link to={link.link} style={{ textDecoration: 'none' }}>
            <UnstyledButton key={link.label} className={classes.mainLink} sx={isActive ? {backgroundColor : theme.colors.gray[2], fontWeight: 700}: {}}>
                <div className={classes.mainLinkInner}>
                <link.icon size={20} className={classes.mainLinkIcon} />
                <span>{link.label}</span>
                </div>
            </UnstyledButton>
        </Link>
   
  )
}
