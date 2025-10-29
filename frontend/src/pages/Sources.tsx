import Navbar from "../components/Navbar";
import Footer from "../components/Footer";

export default function Sources() {
  return (
    <div className="main-layout">
      <Navbar onSearch={() => {}} searchValue="" />

      <main className="main-content">
        <div className="container">
          <div className="page-header">
            <h1>Sources</h1>
            <p>Here you will find all the sources we use for our AI news.</p>
          </div>
          <p style={{ color: "var(--text-muted)", marginTop: "2rem" }}>
            This page is under development. Soon you will find a comprehensive list of all our news sources here.
          </p>
        </div>
      </main>

      <Footer />
    </div>
  );
}
