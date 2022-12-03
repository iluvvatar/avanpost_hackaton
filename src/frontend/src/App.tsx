import React, {useEffect, useState} from 'react';
import './App.css';
import {Layout} from "antd";
import VersionList from "./components/VersionList";
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
        <Layout>
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
            <Footer>Footer</Footer>
        </Layout>
    )
}

export default App;
