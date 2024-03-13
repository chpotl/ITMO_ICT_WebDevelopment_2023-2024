import style from "./SignInPage.module.scss";
import { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

export const SignInPage = () => {
  const [userName, setUsername] = useState<string>("");
  const [password, setPassword] = useState<string>("");
  const [email, setEmail] = useState<string>("");
  const [isLogin, setLogin] = useState<boolean>(false);
  const navigate = useNavigate();

  const handleRegister = async () => {
    try {
      const response = await axios.post("http://127.0.0.1:8000/auth/users/", {
        email: email,
        username: userName,
        password: password,
      });

      if (response.status === 201) {
        const userId = response.data.id;
        localStorage.setItem("authToken", response.data.auth_token);
        localStorage.setItem("userId", userId);
        localStorage.setItem("username", userName);
        alert("Регистрация успешна");
        navigate("/main");
      }
    } catch (error) {
      console.error("Ошибка при регистрации:", error);
    }
  };

  const handleLogin = async () => {
    try {
      const loginResponse = await axios.post(
        "http://127.0.0.1:8000/auth/token/login/",
        {
          username: userName,
          password: password,
        }
      );

      if (loginResponse.status === 200) {
        localStorage.setItem("authToken", loginResponse.data.auth_token);
        const userResponse = await axios.get(
          "http://127.0.0.1:8000/auth/users/me/",
          {
            headers: {
              Authorization: `Token ${loginResponse.data.auth_token}`,
            },
          }
        );

        if (userResponse.status === 200) {
          const userId = userResponse.data.id;
          localStorage.setItem("userId", userId);
          localStorage.setItem("username", userName);
          alert("Вход выполнен успешно");
          navigate("/main");
        }
      }
    } catch (error) {
      console.error("Ошибка при входе:", error);
    }
  };

  return (
    <div className={style.container}>
      <h1>Добро пожаловать в Конференсий</h1>
      <div className={style.signOptions}>
        <p onClick={() => setLogin(false)}>Зарегистрироваться</p>
        <p onClick={() => setLogin(true)}>Войти</p>
      </div>
      <div className={style.inputs}>
        {isLogin == false ? (
          <div className={style.customInput}>
            <p>Email</p>
            <input
              type="email"
              className={style.newInput}
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
          </div>
        ) : (
          <></>
        )}
        <div className={style.customInput}>
          <p>Username</p>
          <input
            className={style.newInput}
            value={userName}
            onChange={(e) => setUsername(e.target.value)}
          />
        </div>
        <div className={style.customInput}>
          <p>Password</p>
          <input
            className={style.newInput}
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </div>
      </div>
      <div className={style.buttons}>
        <button className={style.signButton} onClick={handleRegister}>
          Зарегистрироваться
        </button>
        <button onClick={handleLogin} className={style.signButton}>
          Войти
        </button>
      </div>
    </div>
  );
};
