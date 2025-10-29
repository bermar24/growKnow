import Navbar from "../components/Navbar";
import Footer from "../components/Footer";

export default function About() {
  return (
    <div className="main-layout">
      <Navbar onSearch={() => {}} searchValue="" />

      <main className="main-content">
        <div className="container">
          <div className="page-header">
            <h1>About GrowKnow</h1>
            <p>Your central hub for AI news and learning.</p>
          </div>
          <p style={{ color: "var(--text-muted)", marginTop: "2rem" }}>
            This page is under development. Soon you will find more information about our project and team here.
          </p>
        </div>
      </main>

      <Footer />
    </div>
  );
}
