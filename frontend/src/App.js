import logo from './logo.svg';
import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Home from './components/Home'
import ResultBook from "./components/ResultBook";
import BookDetail from "./components/BookDetail";
import LDAVisualization from "./components/LDAvis";

function App() {
  return (
      <div className="App">
            <BrowserRouter>
                <Routes>
                    <Route exact path='/' element={<Home/>} />
                    <Route path='/search' element={<ResultBook/>} />
                    <Route path='/vis' element={<LDAVisualization/>} />
                    <Route path='/search/:bookTitle' element={<ResultBook/>} />
                    <Route path='/detail/:bookID' element={<BookDetail/>} />
                </Routes>
            </BrowserRouter>
      </div>
  );
}

export default App;