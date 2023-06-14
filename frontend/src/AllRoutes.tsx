import React, { Dispatch, SetStateAction } from 'react';
import { Route, Routes, useLocation, useNavigate, Navigate } from 'react-router-dom';
import Documentation from './pages/Documentation';
import CheckCategory from './pages/CheckCategory';
import CheckList from './pages/CheckList';
import Overview from './pages/Statistics/Overview';
import AppDetail from './pages/Statistics/AppDetail';

import { Breadcrumbs, Anchor } from '@mantine/core';
import SearchApp from './pages/SearchApp';

// Define the type for a policy object
interface Policy {
  [key: string]: number;
}

// Define the type for an app data object
interface PolicyObject {
  id: string;
  name: string;
  image: string;
  policies: Policy;
}

// Define the type for the props passed to the Route component
interface RouteProps {
  appData: PolicyObject[];
  setAppData: Dispatch<SetStateAction<PolicyObject[]>>;
  currentApp: PolicyObject;
  setCurrentApp: Dispatch<SetStateAction<PolicyObject>>;
}

// Capitalizes the first letter of a string
function capitalizeFirstLetter(s: string): string {
  return s.charAt(0).toUpperCase() + s.slice(1);
}

// Generates breadcrumb paths and names from the current location pathname
function generatePaths(array: string[]) {
  let result = [];
  let path = '';

  for (let i = 0; i < array.length; i++) {
    const name = array[i];
    path += `/${name}`;

    result.push({
      name: capitalizeFirstLetter(name),
      path: path.substring(1),
    });
  }

  return result;
}

export default function AllRoutes({appData, setAppData, currentApp, setCurrentApp}: RouteProps) {
  const location = useLocation();
  const navigate = useNavigate();

  // Generate breadcrumb items based on the current path
  const items = generatePaths(
    location.pathname.split('/').filter((value: string) => value !== '')
  ).map((item, index) => (
    <Anchor onClick={() => navigate(item.path)} key={index}>
      {item.name}
    </Anchor>
  ));

  return (
    <>
      {/* Render the breadcrumbs */}
      <Breadcrumbs>{items}</Breadcrumbs>

      <Routes>
        {/* Default route */}
        <Route path="/" element={<Navigate to="/documentation" />} />

        {/* Route components */}
        <Route path="/documentation" element={<Documentation />} />
        <Route
          path="/category"
          element={<CheckCategory setAppData={setAppData} />}
        />
        <Route path="/list" element={<CheckList setAppData={setAppData} />} />
        <Route path="/name" element={<SearchApp setAppData={setAppData} />} />

        {/* Overview routes */}
        <Route
          path="/list/overview"
          element={<Overview appData={appData} setCurrentApp={setCurrentApp} />}
        />
        <Route
          path="/name/overview"
          element={<Overview appData={appData} setCurrentApp={setCurrentApp} />}
        />
        <Route
          path="/category/overview"
          element={<Overview appData={appData} setCurrentApp={setCurrentApp} />}
        />

        {/* App detail routes */}
        <Route
          path="/list/overview/app"
          element={<AppDetail currentApp={currentApp} />}
        />
        <Route
          path="/name/overview/app"
          element={<AppDetail currentApp={currentApp} />}
        />
        <Route
          path="/category/overview/app"
          element={<AppDetail currentApp={currentApp} />}
        />
      </Routes>
    </>
  );
}
