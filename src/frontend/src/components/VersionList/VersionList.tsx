import React, {useState} from "react";
import {NewVersionFormValueTypes, Version} from "../../App";
import {Link} from "react-router-dom";
import {List, Button} from "antd";
import AddVersionModal from "./AddVersionModal";
import classes from './VersionList.module.css'
import UploadTestImage from "./UploadTestImage";


interface VersionListProps {
    versionList: Version[]
}

const VersionList: React.FC<VersionListProps> = (props) => {
    const [isModalOpen, setIsModalOpen] = useState<boolean>(false);
    const [addFormValues, setAddFormValues] = useState<NewVersionFormValueTypes>()

    const showModal = () => {
        setIsModalOpen(true);
    };
    const handleModalOk = (values: NewVersionFormValueTypes) => {
        setAddFormValues(values);
        setIsModalOpen(false);
    };
    const handleModalCancel = () => {
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
            <UploadTestImage/>
            <AddVersionModal
                isModalOpen={isModalOpen}
                onOk={handleModalOk}
                onCancel={handleModalCancel}
            />
        </>
    )
}

export default VersionList;
