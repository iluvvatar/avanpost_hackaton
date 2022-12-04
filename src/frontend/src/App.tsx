import React, {useEffect, useState} from 'react';
import './App.css';
import {Layout} from "antd";
import VersionListPage from "./pages/VersionListPage/VersionListPage";
import {NavLink, Route, Routes} from "react-router-dom";
import MainPage from "./pages/MainPage/MainPage";
import TestPage from "./pages/TestPage/TestPage";
import LearnPage from "./pages/LearnPage/LearnPage";
import axios from 'axios';

const {Footer, Content} = Layout;


export interface SelectOptionType {
    value: string
    label: string
}
export interface Version {
    id: string,
    title: string
}
export interface NewVersionFormValueTypes {
    label: string,
    dataUrl: string
}

function App() {

    let [versionList, setVersionList] = useState<string[]>([])

    useEffect(() => {
        axios.get('http://158.160.47.53:8080/api/v1/versions/list')
            .then(response => {
                setVersionList(response.data.data)
            })
            .catch(err => {
                console.log(err)
            })
    }, [])



    return (
        <Layout className='app-container'>
            <Content className='app-page-content'>
                <Routes>
                    <Route path="/" element={
                        <MainPage/>
                    }/>
                    <Route path="/test" element={
                        <TestPage versionList={versionList}/>
                    }/>
                    <Route path="/learn" element={
                        <LearnPage/>
                    }/>
                    <Route path="/versionList" element={
                        <VersionListPage versionList={versionList}/>
                    }/>
                    {/*<Route path="/versionList/:id" element={*/}
                    {/*    <VersionPage versionList={versionList}/>*/}
                    {/*}/>*/}
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
