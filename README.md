<a name="readme-top"></a>

[![LinkedIn][linkedin-shield]][linkedin-url]
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/natuspati/to-do">
    <img src=images/random_logo.png alt="Logo" width="200" >
  </a>

<h3 align="center">To Do</h3>

  <p align="center">
    A simple backend for a todo app.
  </p>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About the Game</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
      <ul>
        <li><a href="#running-tests">Running tests</a></li>
        <li><a href="#screenshots">Screenshots</a></li>
      </ul>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->

## About the Project

To Do is a basic app for tracking tasks.

* Tasks have name, description and status.
* Status can be pending, completed or cancelled.
* CRUD operations use asynchronous client for MongoDB
* Unit tests cover valid and invalid inputs.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Built With

Back-end is built with FastAPI using Test Driven Development.

* Pytest is chosen for its mature resources and extensive ecosystem of plugins.
* MongoDB is database.
* Motor is asynchronous driver with Pymongo as Object Document Mapper.
* Dependencies are used to isolate logic from routes.

[![FastAPI][fastapi.com]][fastapi-url]
[![MongoDB][MongoDB.com]][MongoDB-url]
[![Pytest][Pytest.com]][Pytest-url]


<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->

## Getting Started

### Pre-requisites

Use `pipenv` package for a deterministic build instead of `pip` and [`requirements.txt`](backend/requirements.txt),
which can be installed with

```sh
pip install pipenv
```

For MongoDB, either a free remote database can be set up using [this link](https://www.mongodb.com/free-cloud-database)
or a local instance can be run following these [instructions](https://www.mongodb.com/docs/manual/installation/).

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/natuspati/to-do.git
   ```
2. Edit [`example.env`](backend/example.env) with MongoDB URL from
   [pre-requisites](#pre-requisites) and create a copy `.env`
   ```sh
   cd to-do/backend
   cp example.env .env
   ```
3. Install packages using `pipenv`
   ```sh
   pipenv install
   ```
   or from [`requirements.txt`](backend/requirements.txt)
   ```sh
      pip install -r requirements.txt
   ```
4. Run `uvicorn` command
   ```sh
   uvicorn app.api.server:app --reload --host 127.0.0.1 --port 8000
   ```
5. Visit http://127.0.0.1:8000/

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->

## Usage

### Running tests

TDD principle dictates
> Write test that fails and add just enough code to make the test pass.

The project uses this principle and extensibility of [`backend/tests/`](backend/tests) shows that.

To run the tests, use the command:

```sh
pytest -v backend/tests 
```

### Screenshots

<p float="left">
  <img src=images/routes.png alt="Default" height="200" >
  <img src=images/list_route.png alt="Default" height="200" >
  <img src=images/put_route.png alt="Default" height="200" >
  <img src=images/schemas.png alt="Default" height="200" >
</p>

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ROADMAP -->

## Roadmap

- [x] Configure asynchronous MongoDB driver that is able to connect/disconnect with the app events
- [x] Configure Pytest with asynchronous test client
- [x] Add Task CRUD endpoints
- [x] Isolate ODM operations to [`repositories`](backend/app/db/repositories)
- [ ] Add user authentication and resouce management
- [ ] Create Behavior Driven Tests from client and cleaner points of view

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- LICENSE -->

## License

Distributed under the MIT License. See [`LICENSE.txt`](LICENSE.txt) for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->

## Contact

Nurlat Bekdullayev - [@natuspati](https://twitter.com/natuspati) - natuspati@gmail.com

Project Link: [https://github.com/natuspati/to-do](https://github.com/natuspati/to-do)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->

## Acknowledgments

Thanks to these resources that helped me to build the game.

* [Aaron Bassett - Getting Started with MongoDB and FastAPI](https://www.mongodb.com/developer/languages/python/python-quickstart-fastapi/)
* [ Jeff Astor's series on FastAPI and React](https://github.com/Jastor11/phresh-tutorial/tree/master).
* [Michael Herman: Developing and Testing an Asynchronous API with FastAPI and Pytest](https://testdriven.io/blog/fastapi-crud/)
* [Othneil Drew: Best-README-Template](https://github.com/othneildrew/Best-README-Template)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->

[contributors-shield]: https://img.shields.io/github/contributors/natuspati/country-guess-game.svg?style=for-the-badge

[contributors-url]: https://github.com/natuspati/country-guess-game/graphs/contributors

[forks-shield]: https://img.shields.io/github/forks/natuspati/country-guess-game.svg?style=for-the-badge

[forks-url]: https://github.com/natuspati/country-guess-game/network/members

[stars-shield]: https://img.shields.io/github/stars/natuspati/country-guess-game.svg?style=for-the-badge

[stars-url]: https://github.com/natuspati/country-guess-game/stargazers

[issues-shield]: https://img.shields.io/github/issues/natuspati/country-guess-game.svg?style=for-the-badge

[issues-url]: https://github.com/natuspati/country-guess-game/issues

[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555

[linkedin-url]: https://www.linkedin.com/in/nurlat/

[license-shield]: https://img.shields.io/github/license/natuspati/country-guess-game.svg?style=for-the-badge

[license-url]: https://github.com/natuspati/country-guess-game/blob/main/LICENSE.txt

[fastapi.com]: https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white

[fastapi-url]: https://fastapi.tiangolo.com/

[MongoDB.com]: https://img.shields.io/badge/MongoDB-47A248?style=for-the-badge&logo=mongodb&logoColor=white

[MongoDB-url]: https://www.mongodb.com/

[Pytest.com]: https://img.shields.io/badge/Pytest-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white

[Pytest-url]: https://docs.pytest.org/en/7.4.x/