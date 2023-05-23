import React, {useState } from 'react';
import './App.css';
import { Navigation } from './Components/Navigation';
import { BrowserRouter } from 'react-router-dom';
import {Vocabulary,User,Checkbox} from 'tabler-icons-react';
import { Grid, ScrollArea } from '@mantine/core';
import AllRoutes from './AllRoutes';


function App() {

  interface NavigationLink{ 
     icon: React.ElementType; 
     label: string ;
     link: string;
  }

  const links : NavigationLink[] = [
    { icon: Vocabulary, label: 'Documentation', link: '/documentation'},
    { icon: Checkbox, label: 'App category', link: '/category'},
    { icon: User, label: 'List of apps', link: '/list'},
    { icon: User, label: 'Name of app', link: '/name'},
  ];

  interface Policy {
    [key: string]: number;
  }
  
  interface PolicyObject {
    id: string;
    name: string;
    image: string;
    policies: Policy;
  }
  
  const [appData, setAppData] = useState<PolicyObject[]>([])
  const [currentApp, setCurrentApp] = useState<PolicyObject>({id: "", name: "", image: "", policies: {}})

  return (
    <BrowserRouter>
      <Grid>
        <Grid.Col span={4} md={3} > 
          <Navigation links={links}/>
        </Grid.Col>
        
        <Grid.Col span={8} md={9} >
           <ScrollArea h="90vh" p={40} >
            <AllRoutes appData={appData} setAppData={setAppData} currentApp={currentApp} setCurrentApp={setCurrentApp} />
          </ScrollArea>
        </Grid.Col>
      </Grid>
    </BrowserRouter>
  );
}

export default App;
