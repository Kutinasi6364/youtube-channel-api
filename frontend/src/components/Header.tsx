// src/components/Navbar.tsx
import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useNavigate } from 'react-router-dom';

const Navbar = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const handleLogout = () => {
    localStorage.removeItem('access_token'); // access_token削除
    localStorage.removeItem('refresh_token'); // refresh_token削除
    navigate('login'); // ログイン画面にリダイレクト
  };

  return (
    <nav className="navbar navbar-expand-lg bg-danger" id="navbar">
      <div className="container-fluid ms-5">
        <Link className="navbar-brand" to="/channels">
          Youtube Channel List
        </Link>

        {/* トグルボタン */}
        <button
          className="navbar-toggler ms-auto"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarNav"
          aria-controls="navbarNav"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span className="navbar-toggler-icon"></span>
        </button>

        {/* リンク一覧 */}
        <div className="collapse navbar-collapse" id="navbarNav">
          <ul className="navbar-nav ms-auto">
            <li className="nav-item">
              <Link className={`nav-link ${location.pathname === '/channels' ? 'active' : ''}`} to="/channels">
                ホーム
              </Link>
            </li>
            <li className="nav-item">
              <Link className={`nav-link ${location.pathname === '/channellist' ? 'active' : ''}`} to="/channellist">
                登録チャンネル一覧
              </Link>
            </li>
            <li className="nav-item">
              <Link className="nav-link" to="/channelsearch">
                チャンネル検索/登録
              </Link>
            </li>
            <li className="nav-item">
              <Link className="nav-link" to="/password_change">
                パスワードリセット
              </Link>
            </li>
            {location.pathname !== '/login' && (
              <li className="nav-item">
                <button onClick={handleLogout} type="submit" className="nav-link">
                  ログアウト
                </button>
              </li>
            )}
          </ul>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
