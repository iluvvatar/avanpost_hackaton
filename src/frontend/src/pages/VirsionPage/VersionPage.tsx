import React from 'react'
import {useParams} from "react-router-dom";
import {Layout} from "antd";

const {Content} = Layout;

interface VersionPageProps {

}

const VersionPage: React.FC<VersionPageProps> = () => {
    const {id} = useParams()

    return (
        <Layout>
            <Content>
                <h3>VersionPage</h3>
                <div>Version id: {id}</div>
                <div>Classes: some classes</div>
                <div>Metrics: some metrics</div>
            </Content>
        </Layout>

    )
}

export default VersionPage
