import React, {useState} from "react";
import {Version} from "../../App";
import {Link} from "react-router-dom";
import {List, Button} from "antd";
import AddVersionModal from "../AddVersionModal";
import classes from './VersionList.module.css'


interface VersionListProps {
    versionList: Version[]
}

const VersionList: React.FC<VersionListProps> = (props) => {

    const [isModalOpen, setIsModalOpen] = useState(false);

    const showModal = () => {
        setIsModalOpen(true);
    };
    const handleOk = () => {
        setIsModalOpen(false);
    };
    const handleCancel = () => {
        setIsModalOpen(false);
    };

    return (
        <>
            <List
                header={
                    <div className={classes.listHeader}>
                        <h2>VersionList</h2>
                        <Button type="primary" onClick={showModal}>
                            Add
                        </Button>
                    </div>
                }
                dataSource={props.versionList}
                renderItem={(version) => (
                    <List.Item>
                        <Link to={`/version/${version.id}`}>{version.title}</Link>
                    </List.Item>
                )}
            />
            <AddVersionModal
                onOk={handleOk}
                onCancel={handleCancel}
                isModalOpen={isModalOpen}
            />
        </>
    )
}

export default VersionList;
