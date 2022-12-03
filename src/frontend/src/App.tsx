import React, {useEffect, useState} from 'react';
import './App.css';
import {Layout} from "antd";
import VersionList from "./components/VersionList/VersionList";
import {v1} from "uuid";
import {Route, Routes} from "react-router-dom";
import VersionPage from "./pages/VirsionPage/VersionPage";

const {Footer, Content} = Layout;

export interface Version {
    id: string,
    title: string
}

function App() {

    let [versionList, setVersionList] = useState<Version[]>([])

    useEffect(() => {
        setVersionList(createVersionList());
    }, [])


    const createVersionList = () => {
        let versionListArr: Version[] = [];
        for (let i = 1; i < 5; i++) {
            versionListArr.push(
                {id: v1(), title: `version ${i}`}
            )
        }
        return versionListArr
    }

    return (
        <Layout className='app-container'>
            <Content>
                <Routes>
                    <Route path="/" element={
                        <VersionList versionList={versionList}/>
                    }/>
                    <Route path="/version/:id" element={
                        <VersionPage/>
                    }/>
                </Routes>
            </Content>
            <Footer>team: Panic! At the kernel for avanpost_hackaton(c)</Footer>
        </Layout>
    )
}

export default App;
