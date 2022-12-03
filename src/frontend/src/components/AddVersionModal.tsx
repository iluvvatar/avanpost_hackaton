import React from "react";
import { Form, Input, Modal } from "antd";

interface AddVersionModalProps {
    isModalOpen: boolean
    onOk: () => void
    onCancel: () => void
}

const AddVersionModal: React.FC<AddVersionModalProps> = (props) => {
    return (
        <Modal title="New version"
               open={props.isModalOpen}
               onOk={props.onOk}
               onCancel={props.onCancel}>
            <Form>
                <Input style={{marginBottom: '10px'}} placeholder="Title of new class"/>
                <Input placeholder="Paste link"/>
            </Form>
        </Modal>
    )
}

export default AddVersionModal;
