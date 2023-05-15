import React from 'react'
import { Route, Routes } from 'react-router-dom';
import Documentation from './pages/Documentation';
import CheckCategory from './pages/CheckCategory';
import CheckList from './pages/CheckList';
import Overview from './pages/Statistics/Overview';

export default function AllRoutes() {
  return (
    <Routes>
      <Route path="/documentation" element={<Documentation />} />
      <Route path="/category" element={<CheckCategory />} />
      <Route path="/list" element={<CheckList />} />

      <Route path="/list/overview" element={<Overview />} />
      <Route path="/category/overview" element={<Overview />} />
    </Routes>
  )
}
