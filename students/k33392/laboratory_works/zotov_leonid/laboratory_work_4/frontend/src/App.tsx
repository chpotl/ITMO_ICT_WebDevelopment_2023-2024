import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { SignInPage } from "./pages/SignInPage";
import { MainPage } from "./pages/MainPage";
import { ConferencePage } from "./pages/ConferencePage";
import { ConferenceCreatePage } from "./pages/ConferenceCreatePage";
import { ConferenceEditPage } from "./pages/ConferenceEditPage";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<SignInPage />}></Route>
        <Route path="main" element={<MainPage />}></Route>
        <Route path="conference/:id" element={<ConferencePage />} />
        <Route
          path="conference_create"
          element={<ConferenceCreatePage />}
        ></Route>
        <Route path="/conference_edit/:id" element={<ConferenceEditPage />} />
      </Routes>
    </Router>
  );
}

export default App;
