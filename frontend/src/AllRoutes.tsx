import React, { Dispatch, SetStateAction } from 'react'
import { Route, Routes } from 'react-router-dom';
import Documentation from './pages/Documentation';
import CheckCategory from './pages/CheckCategory';
import CheckList from './pages/CheckList';
import Overview from './pages/Statistics/Overview';
import AppDetail from './pages/Statistics/AppDetail';

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

export default function AllRoutes({appData, setAppData, currentApp, setCurrentApp}: RouteProps) {
  return (
    <Routes>
      <Route path="/documentation" element={<Documentation />} />
      <Route path="/category" element={<CheckCategory setAppData={setAppData} />} />
      <Route path="/list" element={<CheckList setAppData={setAppData} />} />

      <Route path="/list/overview" element={<Overview appData={appData} setCurrentApp={setCurrentApp}/>} />
      <Route path="/category/overview" element={<Overview appData={appData} setCurrentApp={setCurrentApp} />} />

      <Route path="/list/overview/app" element={<AppDetail currentApp={currentApp}  />} />
      <Route path="/category/overview/app" element={<AppDetail currentApp={currentApp}  />} />

    </Routes>
  )
}
