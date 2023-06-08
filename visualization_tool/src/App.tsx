import logo from '/logo.png';
import './App.css';

function App() {
  return (
    <>
      <div>
        <a
          href="https://github.com/google/gcp_scanner"
          target="_blank"
          rel="noreferrer"
        >
          <img src={logo} className="logo" alt="GCP Scanner logo" />
        </a>
      </div>
      <h1>Hello GCP Scanner!</h1>
    </>
  );
}

export default App;
