import React, { useState } from 'react';
import { Navigation } from './Components/Navigation';
import { BrowserRouter } from 'react-router-dom';
import { Vocabulary, Search, ListCheck, Category } from 'tabler-icons-react';
import { Grid, ScrollArea } from '@mantine/core';
import AllRoutes from './AllRoutes';

function App() {
  // Define the type for navigation links
  interface NavigationLink {
    icon: React.ElementType;
    label: string;
    link: string;
  }

  // Define an array of navigation links
  const links: NavigationLink[] = [
    { icon: Vocabulary, label: 'Documentation', link: '/documentation' },
    { icon: Category, label: 'App category', link: '/category' },
    { icon: ListCheck, label: 'List of apps', link: '/list' },
    { icon: Search, label: 'Search for app', link: '/name' },
  ];

  // Define the type for a policy object
  interface Policy {
    [key: string]: number;
  }

  // Define the type for an app data object
  interface PolicyObject {
    id: string;
    name: string;
    logo_url: string;
    policy: string;
    scores: Policy;
    status: string;
  }

  // Define state variables using the useState hook
  // appData is a list with information about every app which comes from the backend
  // Current App sets the declares, which app is shown in overview/app
  const [appData, setAppData] = useState<PolicyObject[]>([]);
  const [currentApp, setCurrentApp] = useState<PolicyObject>({
    id: '',
    name: '',
    logo_url: '',
    status: '',
    policy: '',
    scores: {},
  });

  return (
    <BrowserRouter>
      <Grid>
        {/* Navigation component */}
        <Grid.Col span={4} md={3}>
          <Navigation links={links} />
        </Grid.Col>

        {/* Main content */}
        <Grid.Col span={8} md={9}>
          <ScrollArea h="90vh" p={40}>
            {/* Render all the routes */}
            <AllRoutes
              appData={appData}
              setAppData={setAppData}
              currentApp={currentApp}
              setCurrentApp={setCurrentApp}
            />
          </ScrollArea>
        </Grid.Col>
      </Grid>
    </BrowserRouter>
  );
}

export default App;
