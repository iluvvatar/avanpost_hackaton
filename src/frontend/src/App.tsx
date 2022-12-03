import React from 'react';
import './App.css';
import {Layout} from "antd";
import VersionListPage from "./pages/VersionListPage/VersionListPage";
import {NavLink, Route, Routes} from "react-router-dom";
import VersionPage from "./pages/VirsionPage/VersionPage";
import MainPage from "./pages/MainPage/MainPage";
import TestPage from "./pages/TestPage/TestPage";
import LearnPage from "./pages/LearnPage/LearnPage";

const {Footer, Content} = Layout;

export interface Version {
    id: string,
    title: string
}

export interface NewVersionFormValueTypes {
    title: string,
    link: string
}

function App() {


    return (
        <Layout className='app-container'>
            <Content className='app-page-content'>
                <Routes>
                    <Route path="/" element={
                        <MainPage/>
                    }/>
                    <Route path="/test" element={
                        <TestPage/>
                    }/>
                    <Route path="/learn" element={
                        <LearnPage/>
                    }/>
                    <Route path="/versionList" element={
                        <VersionListPage/>
                    }/>
                    <Route path="/versionList/:id" element={
                        <VersionPage/>
                    }/>
                </Routes>

            </Content>
            <Footer style={{height: '90px',padding: '0px'}}>
                <NavLink to='/versionList' >
                    version list
                </NavLink>
                <div style={{ marginTop: '30px',}}>team: Panic! At the kernel for </div>
                <div>avanpost_hackaton(c)</div>
            </Footer>
        </Layout>
    )
}

export default App;
