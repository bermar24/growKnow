import Navbar from "../components/Navbar";
import Footer from "../components/Footer";

export default function Admin() {
  return (
    <div className="main-layout">
      <Navbar onSearch={() => {}} searchValue="" />

      <main className="main-content">
        <div className="container">
          <div className="page-header">
            <h1>Admin Panel</h1>
            <p>Admin area for content and user management.</p>
          </div>
          <p style={{ color: "var(--text-muted)", marginTop: "2rem" }}>
            This page is under development. Soon you will find admin functions for managing content and users here.
          </p>
        </div>
      </main>

      <Footer />
    </div>
  );
}
