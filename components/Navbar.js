import React from 'react';
import Link from 'next/link';
import styles from './Navbar.module.css';

const Navbar = () => {
  return (
    <nav className={styles.navbar}>
      <div className={styles.container}>
        <Link href="/" className={styles.logo}>
          Job Matcher
        </Link>
        <ul className={styles.navLinks}>
          <li>
            <Link href="/dashboard" className={styles.navLink}>
              Dashboard
            </Link>
          </li>
          <li>
            <Link href="/rules" className={styles.navLink}>
              Rules
            </Link>
          </li>
        </ul>
      </div>
    </nav>
  );
};

export default Navbar;