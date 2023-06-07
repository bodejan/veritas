import React, { Dispatch, SetStateAction } from 'react'
import { Route, Routes, useLocation, useNavigate, Navigate } from 'react-router-dom';
import Documentation from './pages/Documentation';
import CheckCategory from './pages/CheckCategory';
import CheckList from './pages/CheckList';
import Overview from './pages/Statistics/Overview';
import AppDetail from './pages/Statistics/AppDetail';

import { Breadcrumbs, Anchor } from '@mantine/core';
import SearchApp from './pages/SearchApp';

interface Policy {
  [key: string]: number;
}

interface PolicyObject {
  id: string;
  name: string;
  image: string;
  policies: Policy;
}

interface RouteProps{
  appData: PolicyObject[];
  setAppData: Dispatch<SetStateAction<PolicyObject[]>>;
  currentApp: PolicyObject;
  setCurrentApp: Dispatch<SetStateAction<PolicyObject>>;
}

function capitalizeFirstLetter(s:string):string {
  return s.charAt(0).toUpperCase() + s.slice(1);
}

function generatePaths(array: string[]) {
  let result = [];
  let path = '';
  
  for (let i = 0; i < array.length; i++) {
    const name = array[i];
    path += `/${name}`;
    
    result.push({
      name: capitalizeFirstLetter(name),
      path: path.substring(1)
    });
  }
  
  return result;
}

export default function AllRoutes({appData, setAppData, currentApp, setCurrentApp}: RouteProps) {

  const location = useLocation();
  const navigate = useNavigate();

  const items = generatePaths(location.pathname.split("/").filter((value:string) => value !== "")).map((item, index) => (
    <Anchor onClick={() => navigate(item.path)} key={index}>
      {item.name}
    </Anchor>
  ));
  
  return (
    <>
    <Breadcrumbs>{items}</Breadcrumbs>
    
    <Routes>
    <Route path="/" element={<Navigate to="/documentation" />}/>

      <Route path="/documentation" element={<Documentation />} />
      <Route path="/category" element={<CheckCategory setAppData={setAppData} />} />
      <Route path="/list" element={<CheckList setAppData={setAppData} />} />
      <Route path="/name" element={<SearchApp setAppData={setAppData} />} />

      <Route path="/list/overview" element={<Overview appData={appData} setCurrentApp={setCurrentApp}/>} />
      <Route path="/category/overview" element={<Overview appData={appData} setCurrentApp={setCurrentApp} />} />

      <Route path="/list/overview/app" element={<AppDetail currentApp={currentApp}  />} />
      <Route path="/category/overview/app" element={<AppDetail currentApp={currentApp}  />} />

    </Routes>
    </>
  )
}
