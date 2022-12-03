import React, {useEffect, useState} from 'react';
import './App.css';
import {Layout} from "antd";
import VersionList from "./components/VersionList/VersionList";
import {v1} from "uuid";
import {Route, Routes} from "react-router-dom";
import VersionPage from "./pages/VirsionPage/VersionPage";
import axios from "axios";

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

    let [versionList, setVersionList] = useState<Version[]>([])

    useEffect(() => {
        axios.get('http://158.160.47.53:8080/api/v1/versions')
            .then((data) => {
                console.log(data)
            })

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
            <Footer style={{padding: '0px'}}>
                <div>team: Panic! At the kernel for </div>
                <div>avanpost_hackaton(c)</div>
            </Footer>
        </Layout>
    )
}

export default App;
