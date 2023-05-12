import React from 'react'
import { Route, Routes } from 'react-router-dom';
import Documentation from './pages/Documentation';

export default function AllRoutes() {
  return (
    <Routes>
      <Route path="/documentation" element={<Documentation />} />
    </Routes>
  )
}
