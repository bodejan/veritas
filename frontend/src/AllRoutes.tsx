import React from 'react'
import { Route, Routes } from 'react-router-dom';
import Documentation from './pages/Documentation';
import Category from './pages/Category';

export default function AllRoutes() {
  return (
    <Routes>
      <Route path="/documentation" element={<Documentation />} />
      <Route path="/category" element={<Category />} />
    </Routes>
  )
}
