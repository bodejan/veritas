import React from 'react';
import './App.css';
import { Navigation } from './Components/Navigation';
import { BrowserRouter } from 'react-router-dom';

import {
  Vocabulary,
  User,
  Checkbox,
} from 'tabler-icons-react';
import Documentation from './pages/Documentation';
import { Grid } from '@mantine/core';
import AllRoutes from './AllRoutes';

function App() {

  interface NavigationLink{ 
     icon: React.ElementType; 
     label: string ;
  }

  const links : NavigationLink[] = [
    { icon: Vocabulary, label: 'Documentation'},
    { icon: Checkbox, label: 'App category'},
    { icon: User, label: 'List of apps'},
    { icon: User, label: 'Name of app'},
  ];
  

  return (
   <>

    <Grid>
      <Grid.Col span={4}> 
        <Navigation links={links}/>
      </Grid.Col>
      
      <Grid.Col span={8}>
        <BrowserRouter>
          <AllRoutes />
        </BrowserRouter>
      </Grid.Col>
    </Grid>
   
   </>
  );
}

export default App;
